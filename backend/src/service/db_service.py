from peewee_async import AioModel
from typing_extensions import override, Any
from peewee import Model
from src.domain.model.base_model import db
from .base_service import BaseService
from .log_service import LogService
from src.service.log_service import LogService
from src.domain.model import chat_session_model, user_model, message_history_model

class DBService(BaseService):
    TABLES: list[type[Model]] = [
        chat_session_model.ChatSessionModel, user_model.UserModel, message_history_model.MessageHistoryModel
    ]

    @override
    @classmethod
    @LogService.service_runtime_log(__name__, type_="start")
    async def start(cls) -> None:
        await cls.init_db()


    @override
    @classmethod
    @LogService.service_runtime_log(__name__, type_="end")
    async def end(cls) -> None:
        pass


    @classmethod
    async def init_db(cls) -> None:
        await db.aio_connect()
        LogService.runtime_logger.info("Mysql database connect susccess")
        # safe=True: 有表不创建，没表再创建
        db.create_tables(cls.TABLES, safe=True)


    @classmethod
    async def async_get_or_none(cls, aio_model:AioModel) -> AioModel | None:
        """用于详情接口
        """
        return await aio_model.aio_get_or_none()


    @classmethod
    async def async_save(cls, aio_model: AioModel) -> int:
        """用于创建接口
        """
        rows:int = await aio_model.aio_save()
        return rows


    @classmethod
    async def async_execute(cls, sql_expression:Any) -> Any:
        """用于更新/逻辑删除/列表接口
           更新的sql表达式返回更新的行数
           查列表的sql表达式返回查询的列数
        """
        return db.aio_execute(sql_expression)


    @classmethod
    async def async_execute_sql(cls, sql:str) -> Any:
        """用于复杂sql
        """
        return db.aio_execute_sql(sql)
