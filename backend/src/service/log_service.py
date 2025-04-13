import logging
import queue
import sys
import os
import logging.handlers
from typing import Optional, TypedDict
from logging.handlers import QueueHandler, QueueListener
from enum import Enum
import colorlog
from pythonjsonlogger import jsonlogger
from typing_extensions import override, Dict, List, Any
from .base_service import BaseService


class LoggerConfigType(TypedDict):
    filename: str  # 日志文件名
    level: int     # 日志级别
    dir_suffix: str  # 存储目录后缀


class LoggerEnum(Enum):
    ERROR = "ERROR"
    PERFORMANCE = "PERFORMANCE"
    AUDIT = "AUDIT"
    STATISTICS = "STATISTICS"
    RUNTIME = "RUNTIME"
    SECURITY = "SECURITY"


class LogService(BaseService):
    @override
    @classmethod
    def start(cls) -> None:
        cls.init_log()


    @override
    @classmethod
    def end(cls) -> None:
        # [单线程改造] 停止共享的 QueueListener
        if cls._queue_listener:
            cls._queue_listener.stop()

    # 快捷方式, 拿取对应 logger
    # 错误日志: 记录所有错误和异常堆栈（ERROR 及以上级别）, 日志输出到 log/error
    error_logger = logging.getLogger(LoggerEnum.ERROR.value)
    # 性能日志, 记录接口响应时间、数据库查询耗时等性能指标, 日志输出到 log/performance
    performance_logger = logging.getLogger(LoggerEnum.PERFORMANCE.value)
    # 审计日志, 记录敏感操作（如权限变更、数据删除），用于合规性审查, 日志输出到 log/audit
    audit_logger = logging.getLogger(LoggerEnum.AUDIT.value)
    # 统计日志: 记录业务指标（如用户行为、API 调用次数）, 日志输出到 log/statistics
    statistic_logger = logging.getLogger(LoggerEnum.STATISTICS.value)
    # 安全日志: 记录潜在安全事件（如登录失败、异常 IP 访问）, 日志输出到 log/security
    security_logger = logging.getLogger(LoggerEnum.SECURITY.value)
    # 运行日志: 记录程序运行状态、调试信息、常规操作（如服务启动与关闭、模块加载、debug 信息等） 日志输出到 log/runtime
    runtime_logger = logging.getLogger(LoggerEnum.RUNTIME.value)

    # 日志存放根目录
    LOG_ROOT_DIR: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "..", "log"
    )

    LOG_FORMAT: str = (
        "%(log_color)s%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)d - %(message)s"
    )

    LOG_COLORS: Dict[str, str] = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }

    # 预定义的 logger 配置
    LOGGER_CONFIG: Dict[LoggerEnum, LoggerConfigType] = {
        LoggerEnum.ERROR: {
            "filename": "error.log",
            "level": logging.ERROR,
            "dir_suffix": "error",
        },
        LoggerEnum.PERFORMANCE: {
            "filename": "performance.log",
            "level": logging.INFO,
            "dir_suffix": "performance",
        },
        LoggerEnum.AUDIT: {
            "filename": "audit.log",
            "level": logging.INFO,
            "dir_suffix": "audit",
        },
        LoggerEnum.STATISTICS: {
            "filename": "statistics.log",
            "level": logging.INFO,
            "dir_suffix": "statistics",
        },
        LoggerEnum.SECURITY: {
            "filename": "security.log",
            "level": logging.WARNING,
            "dir_suffix": "security",
        },
        LoggerEnum.RUNTIME: {
            "filename": "runtime.log",
            "level": logging.DEBUG,
            "dir_suffix": "runtime",
        },
    }

    # [单线程改造] 共享的日志队列和单一 QueueListener
    _log_queue: queue.Queue[Any] = queue.Queue()
    _queue_listener: Optional[QueueListener] = None

    @classmethod
    def get_default_console_log_formatter(cls) -> colorlog.ColoredFormatter:
        return colorlog.ColoredFormatter(
            cls.LOG_FORMAT,
            log_colors=cls.LOG_COLORS,
            reset=True,  # 重置颜色（避免影响后续终端输出）
            style="%",   # 使用 % 格式化风格
            secondary_log_colors={},  # 禁用次级颜色
            datefmt="%Y-%m-%d %H:%M:%S",  # 时间格式
        )


    @classmethod
    def get_default_json_log_formatter(cls) -> jsonlogger.JsonFormatter:  # type: ignore
        return jsonlogger.JsonFormatter(  # type: ignore
            fmt=cls.LOG_FORMAT,  # 根据 log_format 定义的字段生成 json
            datefmt="%Y-%m-%d %H:%M:%S",
            json_indent=2,
            json_ensure_ascii=False,  # 是否转义非 ASCII 字符
        )


    @classmethod
    def get_default_console_log_handler(cls) -> logging.Handler:
        return logging.StreamHandler(sys.stdout)


    @classmethod
    def get_default_time_rotating_log_handler(cls, filename: str) -> logging.Handler:
        return logging.handlers.TimedRotatingFileHandler(
            filename=filename,
            interval=1,
            when="D",  # 每天生成新日志
            backupCount=7,  # 日志最多保留七天，七天后归档
            encoding="utf-8",
        )


    @classmethod
    def clean_logger_all_handler(cls, logger: logging.Logger) -> None:
        for handler in logger.handlers:
            logger.removeHandler(handler)


    @classmethod
    def init_log(cls) -> None:
        default_console_log_formatter = cls.get_default_console_log_formatter()
        default_json_log_formatter = cls.get_default_json_log_formatter()

        default_console_log_handler = cls.get_default_console_log_handler()
        default_console_log_handler.setFormatter(default_console_log_formatter)

        # 给根 logger 设置属性，子 logger 会继承属性
        # 默认所有未单独配置的模块 logger，都只会彩色输出到控制台
        root_logger: logging.Logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(default_console_log_handler)

        # [单线程改造] 用于存储所有各 logger 对应的 FileHandler（加了过滤器）
        file_handlers: List[logging.Handler] = []

        # 为每个预定义的 logger 配置设置
        for logger_enum, logger_config in cls.LOGGER_CONFIG.items():
            logger_dir: str = os.path.join(
                cls.LOG_ROOT_DIR, logger_config.get("dir_suffix", "")
            )

            os.makedirs(logger_dir, exist_ok=True)

            # 创建文件处理器
            fh = cls.get_default_time_rotating_log_handler(
                os.path.join(logger_dir, logger_config.get("filename", ""))
            )
            fh.setFormatter(default_json_log_formatter)
            # 添加过滤器，仅处理属于自己的日志记录

            filter = lambda record, name=logger_enum.value: record.name == name
            fh.addFilter(filter)

            file_handlers.append(fh)

            # 获取对应 logger 并设置级别，不再直接添加文件处理器到该 logger
            logger = logging.getLogger(logger_enum.value)
            logger.setLevel(logger_config.get("level", logging.DEBUG))
            logger.propagate = False  # 不使用根 logger 的 handler

            # [单线程改造] 为 logger 添加 QueueHandler，将所有日志输出全推入共享队列
            qh = QueueHandler(cls._log_queue)
            logger.addHandler(qh)

        # QueueListener的逻辑是,每取出一条记录,交给所有的file_handlers处理
        # 然后每个file_handler中绑定了过滤器,确保file_handler只处理数据自己的记录
        cls._queue_listener = QueueListener(cls._log_queue, *file_handlers)
        cls._queue_listener.start()


if __name__ == "__main__":
    LogService.start()

    # 错误日志Demo
    try:
        # 模拟数据库连接失败
        raise ConnectionError(
            "数据库连接失败: 用户 'admin' 无法连接到 10.10.1.100:3306"
        )
    except Exception as e:
        LogService.error_logger.error(
            "数据库连接异常",
            exc_info=True,  # 自动添加异常堆栈
            extra={  # 额外上下文信息
                "component": "database",
                "operation": "connect",
                "retry_count": 3,
            },
        )

    # 性能日志demo
    LogService.performance_logger.info(
        "接口性能指标",
        extra={
            "api_path": "/user",
            "user_id": "412351",
            "http_method": "GET",
            "db_time": "2ms",
        },
    )

    # 审计日志demo
    LogService.audit_logger.info(
        "用户删除操作",
        extra={
            "operator_ip": "127.0.0.1",
            "operation_type": "DELETE_USER",
            "affected_data": {"user_id": "112135", "user_role": "USER"},
        },
    )

    # 安全日志demo
    LogService.security_logger.warning(
        "可疑登录尝试",
        extra={
            "threat_level": "MEDIUM",
            "geo_location": "中国 上海",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        },
    )

    # 运行日志demo
    LogService.runtime_logger.debug(
        "服务初始化配置", extra={"config_hash": "xxxx", "loaded_modules": "api"}
    )


    logger = logging.getLogger(__name__)
    logger.debug("log_service debug")
