from .base_service import BaseService
from peewee_async.aio_model import AioModelSelect, AioModelUpdate
from typing import Any
from src.domain.model.base_model import db, BaseModel
from src.service.log_service import LogService
from src.domain.model import chat_session_model, user_model, message_history_model, model_config
from src.util.time_util import TimeUtil
import peewee

class DBService(BaseService):
    TABLES: list[type[BaseModel]] = [
        chat_session_model.ChatSessionModel,
        user_model.UserModel,
        message_history_model.MessageHistoryModel,
        model_config.ModeConfigModel
    ]

    @classmethod
    @LogService.service_runtime_log(__name__, type_="start")
    async def start(cls) -> None:
        """初始化数据库连接和表结构"""
        await db.aio_connect()
        LogService.runtime_logger.info("MySQL database connected successfully.")
        db.create_tables(cls.TABLES, safe=True)



    @classmethod
    @LogService.service_runtime_log(__name__, type_="end")
    async def end(cls) -> None:
        """关闭连接占位方法"""
        pass



    @classmethod
    async def async_query_detail(cls, query: AioModelSelect) -> BaseModel|None:
        """查询详情（返回单条记录）"""
        try:
            model:BaseModel = await query.aio_get()
            return model
        except peewee.DoesNotExist:
            return None


    @classmethod
    async def async_query_list(cls, query: AioModelSelect) -> list[BaseModel]:
        """查询列表（返回多条记录）"""
        model_list:list[BaseModel] = await cls.async_execute(query)

        return model_list


    @classmethod
    async def async_insert(cls, model_instance: BaseModel) -> None:
        """插入一条记录"""
        now = TimeUtil.now_utc()
        model_instance.gmt_modified = now #type: ignore
        await model_instance.aio_save()


    @classmethod
    async def async_update(cls, update_sql: AioModelUpdate) -> int:
        """更新记录"""
        now = TimeUtil.now_utc()
        gmt_modified_field = update_sql.model.gmt_modified
        update_sql._update.update({gmt_modified_field : now})
        update_rows:int = await cls.async_execute(update_sql)
        return update_rows


    @classmethod
    async def async_logic_delete(cls, update_sql: AioModelUpdate) -> None:
        """逻辑(软)删除记录"""
        update_rows:int = await cls.async_update(update_sql)
        # TODO 这里更换成自定义异常
        assert update_rows >= 1,  "删除失败"


    @classmethod
    async def async_execute(cls, expression: Any) -> Any:
        """执行 peewee SQL 表达式（update/delete/select）"""
        return await db.aio_execute(expression)


    @classmethod
    async def async_execute_sql(cls, raw_sql: str) -> Any:
        """执行原始 SQL 语句"""
        return await db.aio_execute_sql(raw_sql)

    @classmethod
    async def async_count(cls, query: AioModelSelect) -> int:
        """异步执行计数查询，返回记录数"""
        # 使用 Peewee 的 count() 方法执行计数查询
        count = await query.aio_count()
        return count



