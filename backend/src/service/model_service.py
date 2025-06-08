import peewee
from .base_service import BaseService
from src.service.log_service import LogService
from src.util.bean_util import BeanUtil
from typing import Literal, Any
from typing_extensions import override
from src.llm.qwen_plus_latest import QwenPlus, RequestParams as QwenPlusRequestParams
from src.domain.model.model_config import ModeConfigModel, ModelConfigStatus
from src.controller import Pagination
from src.service.db_service import DBService
from src.llm.base_llm import BaseLLM

class ModelService(BaseService):
    @override
    @classmethod
    @LogService.service_runtime_log(__name__, type_="start")
    async def start(cls) -> None:
        pass

    @override
    @classmethod
    @LogService.service_runtime_log(__name__, type_="end")
    async def end(cls) -> None:
        pass

    # 所有的聊天模型要从这里注册,才能使用
    all_model:list[dict[Literal["request_params","instance"], Any]] = [
        {
            "instance": QwenPlus(),
            "request_params": QwenPlusRequestParams()
        }
    ]

    @classmethod
    async def get_model_list(cls) -> list[dict[str, Any]]:
        """获取所有可用的模型
        """
        return [
            {"model_name": model_info["instance"].model_name}
            for model_info in cls.all_model
        ]

    @classmethod
    async def get_model_config_list(
        cls,
        model_name: str|None = None,
        model_status: ModelConfigStatus|None = None,
    ) -> tuple[int, list[ModeConfigModel]]:

        where_query = [
            ModeConfigModel.is_deleted == 0
        ]

        if model_name is not None:
            where_query.append(ModeConfigModel.model_name.contains(model_name))

        if model_status is not None:
            where_query.append(ModeConfigModel.status == model_status)

        sql = ModeConfigModel.select().where(
            *where_query
        ).order_by(
            ModeConfigModel.gmt_create.desc()
        )

        list_ = await DBService.async_query_list(sql)
        total = len(list_)
        return total, list_


    @classmethod
    async def create_model_config(cls, model_config:ModeConfigModel) -> None:
        await cls.check_unique_model_name(model_config)

        local_model_instance:BaseLLM[Any] = list(filter(
            lambda model_info: model_info["instance"].model_name == model_config.model_name,
            cls.all_model
        ))[0]["instance"]

        model_config.platform = local_model_instance.model_platform
        model_config.model_type = local_model_instance.model_type
        model_config.status = ModelConfigStatus.Unconfigured
        model_config.model_doc = local_model_instance.model_doc

        await DBService.async_insert(model_config)

    @classmethod
    async def delete_model(cls, id:str) -> None:
        sql = ModeConfigModel.update(
            is_deleted = 1
        ).where(
            ModeConfigModel.id == id
        )

        await DBService.async_logic_delete(sql)


    @classmethod
    async def check_unique_model_name(
        cls,
        model_config: ModeConfigModel,
        where:list[peewee.Expression] = []
    ) -> None:
        model_name:str = ""

        for model_info in cls.all_model:
            if model_info["instance"].model_name == model_config.model_name:
                model_name = model_config.model_name
                break

        assert bool(model_name) , "当前模型不支持"

        where_query = where + [
            ModeConfigModel.model_name == model_config.model_name,
            ModeConfigModel.is_deleted == 0
        ]

        sql = ModeConfigModel.select().where(*where_query)

        result = await DBService.async_query_detail(sql)

        assert result is None, f"{model_config.model_name}模型已经创建"



