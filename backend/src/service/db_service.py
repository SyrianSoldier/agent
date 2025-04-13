from typing import Optional
from peewee_async import AioModel
from typing_extensions import override, List, Type, Any
from peewee import Model
from src.models.database.base_model import db
from src.models.database.session_model import SessionModel
from .base_service import BaseService
from .log_service import LogService


TABLES: List[Type[Model]] = [SessionModel]


class DBService(BaseService):
    @override
    @classmethod
    def start(cls) -> None:
        cls.init_db()


    @override
    @classmethod
    def end(cls) -> None:
        pass


    @classmethod
    def init_db(cls) -> None:
        db.aio_connect()
        LogService.runtime_logger.info("Mysql database connect susccess")
        # safe=True: 有表不创建，没表再创建
        db.create_tables(TABLES, safe=True)


    @classmethod
    async def async_get_or_none(cls, aio_model:AioModel) -> Optional[AioModel]:
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
