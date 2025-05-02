from typing_extensions import override
from .base_service import BaseService
from src.service.log_service import LogService
from src.domain.model.message_history_model import MessageHistoryModel
from src.service.db_service import DBService
from src.domain.vo.chat_session_vo import ChatSessionListItemVo
from src.domain import model_to_vo

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
    async def create_chat_session(cls, title: str, user_id:int) -> None:
        model = ChatSessionModel(title=title, create_user=user_id)
        await DBService.async_save(model)


    @classmethod
    async def delete_chat_session(cls, id: int) -> None:
       sql =  ChatSessionModel.update(
           is_deleted = 1
       ).where(
            (ChatSessionModel.id == id) &
            (ChatSessionModel.is_deleted  == 0)
        )

       await DBService.async_execute(sql)


    @classmethod
    async def rename_chat_session_title(cls, id: int, title: str) -> None:
        sql = ChatSessionModel.update(
            title = title
        ).where(
            (ChatSessionModel.id == id) &
            (ChatSessionModel.is_deleted  == 0)
        )

        await DBService.async_execute(sql)


    @classmethod
    async def get_chat_session_list(cls, pagesize:int, pagenum:int) -> tuple[int, list[ChatSessionListItemVo]]:
        sql = ChatSessionModel.select().where(
            ChatSessionModel.is_deleted == 0
        ).offset(
            (pagenum - 1) * pagesize
        ).limit(
            pagesize
        ).order_by(
            ChatSessionModel.gmt_motified.desc()
        )

        chat_session_list:list[ChatSessionModel] =  await DBService.async_execute(sql)
        # TODO: FIX type hint
        chat_session_vo_list:list[ChatSessionListItemVo] = [
            await model_to_vo(item, ChatSessionListItemVo)
            for item in chat_session_list
        ]
        totol:int = len(chat_session_vo_list)

        return totol, chat_session_vo_list
