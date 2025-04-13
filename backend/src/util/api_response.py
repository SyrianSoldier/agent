from typing_extensions import  TypeVar, Generic, Optional, TypedDict

DataType = TypeVar('DataType')

class ResponseType(TypedDict, Generic[DataType]):
    code: int
    success: bool
    message: str
    data: Optional[DataType]


class ApiResponse(Generic[DataType]):
    @classmethod
    def success(cls, data: Optional[DataType] = None, message: str = "success", code: int = 200) -> ResponseType[DataType]:
        return {
            "code":code,
            "message": message,
            "data": data,
            "success":True
        }

    @classmethod
    def failed(cls, data: Optional[DataType] , message: str = "failed", code: int = 400) -> ResponseType[DataType]:
        return {
            "code":code,
            "message": message,
            "data": data,
            "success":False
        }
