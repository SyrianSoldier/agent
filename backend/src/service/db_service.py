from peewee_async import AioModel
from peewee_async.aio_model import AioModelSelect, AioModelUpdate
from typing import Any
from src.domain.model.base_model import db, BaseModel
from src.service.log_service import LogService
from src.domain.model import chat_session_model, user_model, message_history_model
from src.util.time_util import TimeUtil


class DBService:
    TABLES: list[type[BaseModel]] = [
        chat_session_model.ChatSessionModel,
        user_model.UserModel,
        message_history_model.MessageHistoryModel,
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
    async def async_query_detail(cls, query: AioModelSelect) -> BaseModel | None:
        """查询详情（返回单条记录）"""
        model:BaseModel | None = await query.get_or_none()
        return model


    @classmethod
    async def async_query_list(cls, query: AioModelSelect) -> list[BaseModel]:
        """查询列表（返回多条记录）"""
        model_list:list[BaseModel] = await query.execute()
        return model_list


    @classmethod
    async def async_insert(cls, model_instance: BaseModel) -> None:
        """插入一条记录"""
        now = TimeUtil.now_str()
        model_instance.gmt_create = now
        model_instance.gmt_modified = now
        await model_instance.aio_save()


    @classmethod
    async def async_update(cls, update_sql: AioModelUpdate) -> None:
        """更新一条记录"""
        now = TimeUtil.now_str()
        update_sql = update_sql.dicts().clone()
        update_sql._update.update({'gmt_modified': now})
        update_rows:int = await cls.async_execute(update_sql)

        # TODO 这里断言, 更新行数不为1就抛异常

    @classmethod
    async def async_batch_update(cls, update_sql: AioModelUpdate) -> int:
        """更新多条记录"""
        # TODO
        raise NotImplementedError()



    @classmethod
    async def async_logic_delete(cls, update_sql: AioModelUpdate) -> None:
        """逻辑删除或标记删除，可视情况调整"""
        return await cls.async_update(update_sql)


    @classmethod
    async def async_execute(cls, expression: Any) -> Any:
        """执行 peewee SQL 表达式（update/delete/select）"""
        return await db.aio_execute(expression)


    @classmethod
    async def async_execute_sql(cls, raw_sql: str) -> Any:
        """执行原始 SQL 语句"""
        return await db.aio_execute_sql(raw_sql)

