import inspect
import peewee
from typing import Optional, Type
import tornado.web
from dataclasses import is_dataclass, fields
from typing_extensions import Generic, Any, Dict
from src.util.api_response import ApiResponse
from src.constants.status_code import HTTPStatusCode, BizStatusCode

class BaseController(tornado.web.RequestHandler):
    """http请求基本handler
    """
    def return_success(
        self,
        data: Any = None,
        http_code: HTTPStatusCode=HTTPStatusCode.OK,
        biz_code: BizStatusCode = BizStatusCode.SUCCESS,
        message: str = BizStatusCode.SUCCESS.description
    ) -> None:
        """请求成功时候调用此方法返回信息
        """
        self.set_status(http_code)

        response = ApiResponse.success(data=data, code=biz_code, message=message)

        self.write(dict(response))


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


    # def _parse_request_body(
    #         self, body_dict:Dict[str,Any], target_cls: Type[RequestBodyMapClassT]
    # ) -> RequestBodyMapClassT:
    #     """将请求体字典转换为目标类型实例(支持 dataclass 或 peewee.Model)
    #        :param data: 请求体字典
    #        :param target_cls: 目标类型(dataclass 或 peewee.Model)子类
    #        :return: 目标类型实例
    #     """
    #     if inspect.isclass(target_cls) and issubclass(target_cls, peewee.Model):
    #         return self. _parse_peewee_model(body_dict, target_cls)
    #     elif is_dataclass(target_cls):
    #         return self._parse_dataclass(body_dict, target_cls)
    #     else:
    #         raise TypeError(f"Unsupported target type: {target_cls}")



    # def _parse_peewee_model(
    #         self, body_dict:Dict[str,Any], model_cls: Type[peewee.Model]
    # ) -> RequestBodyMapClassT:
    #     #
    #     model_fields = model_cls._meta.fields
    #     create_data:Dict[str, Any] = {}

    #     for field_name, field in model_fields.items():
    #         value:Any = body_dict.get(field_name)

    #         # 处理外键关系（例如 user_id → User）
    #         if isinstance(field, peewee.ForeignKeyField):
    #             related_model = field.rel_model
    #             if isinstance(value, dict):
    #                 # 嵌套创建关联模型
    #                 related_instance = self._parse_peewee_model(value, related_model)
    #                 create_data[field.name] = related_instance
    #             elif isinstance(value, int):
    #                 # 直接使用外键ID
    #                 create_data[field.name] = value
    #             else:
    #                 raise ValueError(f"Invalid value for foreign key {field_name}")
    #         else:
    #             create_data[field_name] = value

    #     return model_cls(**create_data) #type: ignore



    # def _parse_dataclass(
    #     self,
    #     data: Dict[str, Any],
    #     target_cls: Type[RequestBodyMapClassT]
    # ) -> RequestBodyMapClassT:
    #     """解析dataclass, 支持嵌套结构"""
    #     field_types = {f.name: f.type for f in fields(target_cls)}
    #     init_data = {}

    #     for name, field_type in field_types.items():
    #         value = data.get(name)

    #         # 处理可选字段
    #         if value is None and self._is_optional(field_type):
    #             init_data[name] = None
    #             continue

    #         # 处理嵌套dataclass
    #         if is_dataclass(field_type):
    #             if not isinstance(value, dict):
    #                 raise TypeError(f"字段 {name} 需要字典类型")
    #             init_data[name] = self._parse_dataclass(value, field_type)

    #         # 处理嵌套列表
    #         elif get_origin(field_type) is list:
    #             init_data[name] = self._parse_list(field_type, value)

    #         # 处理基础类型
    #         else:
    #             init_data[name] = self._cast_value(value, field_type)

    #     return cast(RequestBodyMapClassT, target_cls(**init_data))


    # def _parse_list(self, field_type: Type, value: Any) -> list:
    #     """解析列表类型字段"""
    #     if not isinstance(value, list):
    #         raise TypeError("需要列表类型数据")

    #     item_type = get_args(field_type)[0]
    #     return [self._parse_item(item_type, item) for item in value]


    # def _parse_item(self, item_type: Type, value: Any) -> Any:
    #     """解析列表项"""
    #     if is_dataclass(item_type):
    #         if not isinstance(value, dict):
    #             raise TypeError("列表项需要字典类型")
    #         return self._parse_dataclass(value, item_type)
    #     return self._cast_value(value, item_type)



    # def _cast_value(self, value: Any, target_type: Type) -> Any:
    #     """类型转换处理"""
    #     try:
    #         # 处理特殊类型转换（如字符串转枚举）
    #         if inspect.isclass(target_type) and issubclass(target_type, Enum):
    #             return target_type(value)
    #         return target_type(value)
    #     except (TypeError, ValueError) as e:
    #         raise TypeError(
    #             f"无法将值 {value!r} 转换为类型 {target_type.__name__}"
    #         ) from e



    # def _is_optional(self, field_type: Type) -> bool:
    #     """判断是否为Optional类型"""
    #     return get_origin(field_type) is Union and type(None) in get_args(field_type)
