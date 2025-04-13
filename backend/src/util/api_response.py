from typing_extensions import TypedDict, Any


class ResponseType(TypedDict):
    code: int
    success: bool
    message: str
    data: Any


class ApiResponse():
    @classmethod
    def success(cls, data: Any = None, message: str = "success", code: int = 200) -> ResponseType:
        return {
            "code":code,
            "message": message,
            "data": data,
            "success":True
        }

    @classmethod
    def failed(cls, data: Any , message: str = "failed", code: int = 400) -> ResponseType:
        return {
            "code":code,
            "message": message,
            "data": data,
            "success":False
        }
