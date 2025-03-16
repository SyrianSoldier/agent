import json
from typing import Any, TypeVar, Generic, Optional, TypedDict

T = TypeVar('T')

class ResponseType(TypedDict):
    status_code: int
    succcess: bool
    message: str
    data: Any

class ApiResponse(Generic[T]):
    @staticmethod
    def success(message: str = "Success", data: Optional[T] = None, status_code: int = 200) -> str:
        response:ResponseType = {
            "succcess":True,
            "message": message,
            "data": data,
            "status_code": status_code
        }

        return json.dumps(response)

    @staticmethod
    def error(message: str = "Error", data: Optional[T] = None, status_code: int = 400) -> str:
        response:ResponseType = {
            "succcess":False,
            "message": message,
            "data": data,
            "status_code": status_code
        }
        return json.dumps(response)
