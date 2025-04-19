from typing_extensions import Any
from .dto.base_dto import BaseDto
from .model.base_model import BaseModel
from .vo.base_vo import BaseVo
from dataclasses import asdict, fields as dataclass_fields


async def json_to_dto(json: dict[str, Any], dto_cls: type[BaseDto]) -> BaseDto:
    """标准流程: 前端传递json, 在controller层将json转成dto,交付给service层"""
    return dto_cls(**json)


async def dto_to_model(dto: BaseDto, model_cls: type[BaseModel]) -> BaseModel:
    """标准流程: 用dto接收前端数据, 在service层将dto转成model与数据库交互"""
    return model_cls(**dto.dict())


async def model_to_vo(model: BaseModel, vo_cls: type[BaseVo]) -> BaseVo:
    """标准流程: 将model对象转成vo对象返回前端"""
    model_dict = dict(model.__data__) # __data__ 是 Peewee 的内部属性，它只包含模型字段，不包含方法、外键引用、虚拟字段等。
    vo_fields = {f.name for f in dataclass_fields(vo_cls)}
    vo_init_dict = {k: v for k, v in model_dict.items() if k in vo_fields}
    return vo_cls(**vo_init_dict)


async def vo_to_json(vo: BaseVo) -> dict[str, Any]:
    """标准流程: 将vo转成字典交给tornado返回给前端"""
    return asdict(vo)
