from enum import IntEnum

class HTTPStatusCode(IntEnum):
    """
    HTTP 状态码枚举类
    包含标准状态码和推荐业务描述，支持直接获取状态码数值和描述文本
    示例：
        status = HTTPStatusCode.OK
        print(status)          # HTTPStatusCode.OK
        print(status.value)    # 200
        print(status.code)     # 200 (与 value 相同)
        print(status.description)  # "请求成功"
    """
    # 2xx Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # 3xx Redirection
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304

    # 4xx Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

    @property
    def code(self) -> int:
        """直接获取状态码数值 (与 value 相同)"""
        return self.value

    @property
    def description(self) -> str:
        """获取状态码描述文本"""
        return _http_status_descriptions.get(self.value, "未知状态码")

    @classmethod
    def get_description(cls, code: int) -> str:
        """根据状态码获取描述文本"""
        return _http_status_descriptions.get(code, "未知状态码")

# 状态码描述映射表
_http_status_descriptions = {
    # 2xx
    200: "请求成功",
    201: "资源创建成功",
    202: "请求已接受处理",
    204: "操作成功但无返回内容",

    # 3xx
    301: "资源已永久移动",
    302: "资源临时重定向",
    303: "请使用 GET 方法查看新资源",
    304: "资源未修改",

    # 4xx
    400: "请求参数错误",
    401: "身份验证失败",
    403: "无访问权限",
    404: "资源不存在",
    405: "请求方法不允许",
    409: "资源状态冲突",
    422: "参数验证失败",
    429: "请求过于频繁",

    # 5xx
    500: "服务器内部错误",
    501: "功能未实现",
    502: "网关错误",
    503: "服务不可用",
    504: "网关超时"
}



class BizStatusCode(IntEnum):
    """
    AI Agent 业务状态码枚举类
    编码规则：
    - 2000~2999: 成功及流程状态
    - 4000~4999: 客户端/输入相关错误
    - 5000~5999: 服务端/处理相关错误
    - 6000~6999: 第三方服务错误
    """
    # ================= 成功状态 (2000~2999) =================
    SUCCESS = 2000                     # 通用成功
    TASK_QUEUED = 2001                 # 任务已进入队列
    PROCESSING = 2002                  # 任务处理中
    PARTIAL_SUCCESS = 2003             # 部分成功
    WAITING_USER_INPUT = 2101          # 等待用户输入

    # ================= 客户端错误 (4000~4999) =================
    INVALID_INPUT = 4001               # 输入数据不合法
    INPUT_TOO_LONG = 4002              # 输入内容超长
    SENSITIVE_CONTENT = 4003           # 输入含敏感内容
    QUOTA_EXCEEDED = 4004              # 额度不足
    CONCURRENCY_LIMIT = 4005           # 并发限制
    SESSION_EXPIRED = 4006             # 会话过期
    UNSUPPORTED_MODEL = 4007           # 不支持的模型类型

    # ================= 服务端错误 (5000~5999) =================
    FAILED = 5000                      # 通用失败
    MODEL_LOAD_FAILED = 5001           # 模型加载失败
    INFERENCE_ERROR = 5002             # 模型推理错误
    DEPENDENCY_ERROR = 5003            # 依赖服务故障
    TIMEOUT = 5004                     # 处理超时
    KNOWLEDGE_BASE_ERROR = 5005        # 知识库查询失败
    MEMORY_OVERFLOW = 5006             # 记忆体溢出
    TASK_CHAIN_BROKEN = 5007           # 任务链中断

    # ================= 第三方服务错误 (6000~6999) =================
    LLM_SERVICE_ERROR = 6001           # 大模型服务异常
    VECTOR_DB_ERROR = 6002             # 向量数据库异常
    TTS_FAILED = 6003                  # 语音合成失败
    ASR_FAILED = 6004                  # 语音识别失败

    @property
    def code(self) -> int:
        """获取状态码数值"""
        return self.value

    @property
    def description(self) -> str:
        """获取状态描述"""
        return _biz_status_descriptions.get(self.value, "未知业务状态")

    @classmethod
    def get_description(cls, code: int) -> str:
        """根据状态码获取描述"""
        return _biz_status_descriptions.get(code, "未知业务状态")

# 业务状态码描述映射表
_biz_status_descriptions = {
    # 成功状态
    2000: "操作成功",
    2001: "任务已进入处理队列",
    2002: "任务正在处理中",
    2003: "部分操作执行成功",
    2101: "需要用户补充输入",

    # 客户端错误
    4001: "输入数据格式不符合要求",
    4002: "输入内容长度超过限制",
    4003: "输入包含敏感内容",
    4004: "API调用额度不足",
    4005: "超过最大并发处理数量",
    4006: "会话已过期，请重新发起",
    4007: "不支持的模型类型",

    # 服务端错误
    5000: "操作失败",
    5001: "模型加载失败，请联系管理员",
    5002: "模型推理过程发生错误",
    5003: "依赖服务通信异常",
    5004: "处理超时，请重试",
    5005: "知识库检索失败",
    5006: "上下文记忆容量溢出",
    5007: "任务流程链意外中断",

    # 第三方服务错误
    6001: "大模型服务暂时不可用",
    6002: "向量数据库操作失败",
    6003: "语音合成服务异常",
    6004: "语音识别服务异常"
}
