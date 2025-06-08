import peewee
from .base_model import BaseModel, PeeweeFieldExtend
from enum import Enum, auto
from dataclasses import dataclass
from src.llm.base_llm import ModelPlatform, ModelType

class ModelConfigStatus(Enum):
    Unconfigured = "Unconfigured"
    Configured = "Configured"


class ModeConfigModel(BaseModel):
    model_name:str = peewee.CharField(
        max_length=256,
        null=False,
        unique=True,
        verbose_name="模型名称",
    )

    platform:ModelPlatform= PeeweeFieldExtend.EnumField(
        ModelPlatform,
        null=False,
        verbose_name="模型平台"
    )

    model_type:ModelType= PeeweeFieldExtend.EnumField(
        ModelType,
        null=False,
        verbose_name="模型类型,枚举.云端/本地"
    )

    status: ModelConfigStatus = PeeweeFieldExtend.EnumField(
        ModelConfigStatus,
        default = ModelConfigStatus.Unconfigured,
        null=False,
        verbose_name="模型配置状态"
    )

    model_doc:str = peewee.CharField(
        max_length=256,
        null=True,
        unique=True,
        verbose_name="模型文档地址",
    )

    config_detail: str = peewee.TextField(
        null=True,
        verbose_name= "模型配置json"
    )


    class Meta:
        table_name="model_config"

    def __repr__(self) -> str:
        return super().__repr__()
