from typing import Optional
import tornado.web
from typing_extensions import Generic, List, TypeVar, TypedDict
from src.util.api_response import ApiResponse
from src.constants.status_code import HTTPStatusCode, BizStatusCode
from src.types.response_type import DataType


class BaseController(tornado.web.RequestHandler, Generic[DataType]):
    """http请求基本handler
    """
    def return_success(
        self,
        data: Optional[DataType] = None,
        http_code: HTTPStatusCode=HTTPStatusCode.OK,
        biz_code: BizStatusCode = BizStatusCode.SUCCESS,
        message: str = BizStatusCode.SUCCESS.description
    ) -> None:
        self.set_status(http_code)

        response = ApiResponse.success(data=data, code=biz_code, message=message)

        self.write(dict(response))
        self.finish()


    def return_failed(
        self,
        biz_code: BizStatusCode = BizStatusCode.FAILED,
        message: str = BizStatusCode.FAILED.description,
        http_code: HTTPStatusCode=HTTPStatusCode.INTERNAL_SERVER_ERROR,
        data: Optional[DataType] = None,
    ) -> None:
        self.set_status(http_code)
        response = ApiResponse.failed(data=data, code=biz_code, message=message)

        self.write(dict(response))
        self.finish()

