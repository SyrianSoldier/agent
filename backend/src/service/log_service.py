from enum import Enum
import logging
import sys
import os
import logging.handlers
from typing import TypedDict
import colorlog
from pythonjsonlogger import jsonlogger
from typing_extensions import override, Dict, List, Any
from .base_service import BaseService


class LoggerConfigType(TypedDict):
    filename: str  # 日志文件名
    level: int  # 日志级别
    dir_suffix: str  # 存储目录后缀


class LoggerEnum(Enum):
    ERROR = "ERROR"
    PERFORMANCE = "PERFORMANCE"
    AUDIT = "AUDIT"
    STATISTICS = "STATISTICS"
    RUNTIME = "RUNTIME"
    SECURITY = "SECURITY"


class LogService(BaseService):
    # 快捷方式, 拿取对应logger
    # 错误日志: 记录所有错误和异常堆栈（ERROR及以上级别）, 日志输出到log/error
    error_logger = logging.getLogger(LoggerEnum.ERROR.value)
    # 性能日志, 记录接口响应时间、数据库查询耗时等性能指标, 日志输出到log/performance
    performance_logger = logging.getLogger(LoggerEnum.PERFORMANCE.value)
    # 审计日志, 记录敏感操作（如权限变更、数据删除），用于合规性审查, 日志输出到log/audit
    audit_logger = logging.getLogger(LoggerEnum.AUDIT.value)
    # 统计日志: 记录业务指标（如用户行为、API调用次数）,日志输出到log/statistic
    statistic_logger = logging.getLogger(LoggerEnum.STATISTICS.value)
    # 安全日志: 记录潜在安全事件（如登录失败、异常IP访问）,日志输出到log/security
    security_logger = logging.getLogger(LoggerEnum.SECURITY.value)
    # 运行日志: 记录程序运行状态、调试信息、常规操作（如服务启动与关闭、模块加载、debug信息等） 日志输出到log/runtime
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

    # 预定义的logger配置
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

    @override
    def start(self) -> None:
        self.init_log()

    @override
    def end(self) -> None:
        pass

    def get_default_console_log_formatter(self) -> colorlog.ColoredFormatter:
        return colorlog.ColoredFormatter(
            self.__class__.LOG_FORMAT,
            log_colors=self.__class__.LOG_COLORS,
            reset=True,  # 重置颜色（避免影响后续终端输出）
            style="%",  # 使用 % 格式化风格
            secondary_log_colors={},  # 禁用次级颜色
            datefmt="%Y-%m-%d %H:%M:%S",  # 时间格式
        )

    def get_default_json_log_formatter(self) -> jsonlogger.JsonFormatter:  # type: ignore
        return jsonlogger.JsonFormatter(  # type: ignore
            fmt=self.__class__.LOG_FORMAT,  # 根据log_format定义的字段生成json
            # rename_fields={"levelname": "severity", "asctime": "timestamp"}, # 将log_format定义的字段重命名
            datefmt="%Y-%m-%d %H:%M:%S",
            json_indent=2,
            json_ensure_ascii=False,  # 是否转义非 ASCII 字符（中文等建议设为 False）
        )

    def get_default_console_log_handler(self) -> logging.Handler:
        return logging.StreamHandler(sys.stdout)

    def get_default_time_rotating_log_handler(self, filename: str) -> logging.Handler:
        return logging.handlers.TimedRotatingFileHandler(
            filename=filename,
            interval=1,
            when="D",  # 每天生成新日志
            backupCount=7,  # 日志最多保留七天, 七天后存档
            encoding="utf-8",
        )

    def clean_logger_all_handler(self, logger: logging.Logger) -> None:
        for handler in logger.handlers:
            logger.removeHandler(handler)


    def init_log(self) -> None:
        default_console_log_formatter = self.get_default_console_log_formatter()
        default_json_log_formatter = self.get_default_json_log_formatter()

        default_console_log_handler = self.get_default_console_log_handler()
        default_console_log_handler.setFormatter(default_console_log_formatter)

        # 给根logger设置属性, 子logger会继承属性
        # 默认所有未单独配置的模块logger, 都只会彩色输出到控制台
        root_logger: logging.Logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(default_console_log_handler)

        # 单独为其他logger设置
        logger_enum: LoggerEnum
        logger_config: LoggerConfigType
        for logger_enum, logger_config in self.__class__.LOGGER_CONFIG.items():
            logger_dir: str = os.path.join(
                self.LOG_ROOT_DIR, logger_config.get("dir_suffix", "")
            )

            os.makedirs(logger_dir, exist_ok=True)

            default_time_rotating_log_handler = (
                self.get_default_time_rotating_log_handler(
                    os.path.join(logger_dir, logger_config.get("filename", ""))
                )
            )

            # 默认所有单独配置的logger, 使用json格式保存信息, 并按天轮转日志
            default_time_rotating_log_handler.setFormatter(default_json_log_formatter)
            logger = logging.getLogger(logger_enum.value)
            logger.setLevel(logger_config.get("level", logging.DEBUG))
            logger.addHandler(default_time_rotating_log_handler)
            logger.propagate = False  # 不使用根logger的handler


if __name__ == "__main__":
    log_service = LogService()
    log_service.start()

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
