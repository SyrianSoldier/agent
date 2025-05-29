from typing_extensions import override
from .base_service import BaseService
from src.service.log_service import LogService
from src.service.db_service import DBService
from src.domain.model.message_history_model import MessageHistoryModel, ChatRole
from src.service.chat_serssion_service import ChatSeesionService
from src.domain.dto.chat_session_dto import ChatSessionDetailDto

class MessageHistoryService(BaseService):
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

    @classmethod
    async def get_chat_history_list(cls, session_uuid:str) -> list[MessageHistoryModel]:
        await cls.check_session_exist(session_uuid)

        sql = MessageHistoryModel.select().where(
            MessageHistoryModel.session_uuid == session_uuid
        ).order_by(
            MessageHistoryModel.gmt_create.asc()
        )
        return await DBService.async_query_list(sql)



    @classmethod
    async def create_chat_history(
        cls,
        message_history: MessageHistoryModel
    ) -> None:
        await cls.check_session_exist(message_history.session_uuid)
        await DBService.async_insert(message_history)


    @classmethod
    async def check_session_exist(cls, session_uuid:str) -> None:
        # TODO: 优化代码, 将dto去掉
        dto = ChatSessionDetailDto(uuid = session_uuid)
        session = await ChatSeesionService.get_chat_session_detail(dto)
        assert session is not None, "聊天会话不存在"
