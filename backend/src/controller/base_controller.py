import json
from typing import Any,Literal, override
import tornado.web
from src.util.api_response import ApiResponse
from src.constants.status_code import HTTPStatusCode, BizStatusCode
from src.domain.vo.base_vo import BaseVo
from src.util.bean_util import BeanUtil

type Pagination = dict[
    Literal["pagesize", "pagenum"],
    int
]

type Pagesize = int
type Pagenum = int


class BaseController(tornado.web.RequestHandler):
    """http请求基本handler
    """
    @override
    def prepare(self) -> None:
        self.set_header('Content-Type', 'application/json')


    @override
    def write_error(self, status_code:int, **kwargs:Any) -> None:
        exception_info:tuple[type[Exception], Exception] | None = kwargs.get("exc_info", None)
        # TODO: 出错误的时候向前端返回错误信息即可, 已经实现了, 但是要向日志中写入堆栈报错日志
        if exception_info and isinstance(exception_info[1], Exception):
            exception_msg:str = exception_info[1].args[0]
            self.return_failed(message=exception_msg)


    def return_success(
        self,
        data: BaseVo | None = None,
        http_code: HTTPStatusCode=HTTPStatusCode.OK,
        biz_code: BizStatusCode = BizStatusCode.SUCCESS,
        message: str = BizStatusCode.SUCCESS.description
    ) -> None:
        """请求成功时候调用此方法返回信息
        """
        self.set_status(http_code)

        json_data = (
            data
            if data is None
            else BeanUtil.to_bean(data, dict)
        )

        response = ApiResponse.success(data=json_data, code=biz_code, message=message)

        self.write(dict(response))

        self.finish()



    def return_failed(
        self,
        biz_code: BizStatusCode = BizStatusCode.FAILED,
        message: str = BizStatusCode.FAILED.description,
        http_code: HTTPStatusCode=HTTPStatusCode.INTERNAL_SERVER_ERROR,
        data: Any= None,
    ) -> None:
        """请求失败时候调用此方法返回信息
        """
        self.set_status(http_code)

        response = ApiResponse.failed(data=data, code=biz_code, message=message)

        self.write(dict(response))

        self.finish()



    def request_body_to_dto[T](self, dto_class:type[T]) -> T:
        json_data = json.loads(self.request.body.decode("utf-8"))  # 转字典
        return BeanUtil.to_bean(json_data, dto_class)



    async def get_query_arguments_for_pagination(self) -> Pagination:
        pagesize:int = int(self.get_query_argument("pagesize", default=10)) #type: ignore
        pagenum: int = int(self.get_query_argument("pagenum", default=1))   #type: ignore

        pagintion:Pagination = {
            "pagesize": pagesize,
            "pagenum": pagenum
        }

        return pagintion
