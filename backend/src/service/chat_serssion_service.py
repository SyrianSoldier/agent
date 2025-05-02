from typing_extensions import override
from .base_service import BaseService
from src.service.log_service import LogService
from src.domain.model.chat_session_model import ChatSessionModel
from src.service.db_service import DBService
from src.domain.vo.chat_session_vo import ChatSessionListItemVo
from src.domain.dto.chat_session_dto import ChatSessionCreateDto, ChatSessionDeleteDto, ChatSessionRenameDto
from src.domain.dto.base_dto import PaginationDto

class SeesionService(BaseService):
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
    async def create_chat_session(cls, dto: ChatSessionCreateDto) -> None:
        model = ChatSessionModel(title=dto.title, create_user=dto.user_id)
        await DBService.async_save(model)


    @classmethod
    async def delete_chat_session(cls, dto: ChatSessionDeleteDto) -> None:
       sql =  ChatSessionModel.update(
           is_deleted = 1
       ).where(
            (ChatSessionModel.uuid == dto.uuid) &
            (ChatSessionModel.is_deleted  == 0)
        )

       await DBService.async_execute(sql)


    @classmethod
    async def rename_chat_session_title(cls, dto:ChatSessionRenameDto) -> None:
        sql = ChatSessionModel.update(
            title = dto.title
        ).where(
            (ChatSessionModel.uuid == dto.uuid) &
            (ChatSessionModel.is_deleted  == 0)
        )

        await DBService.async_execute(sql)


    @classmethod
    async def get_chat_session_list(cls, dto: PaginationDto) -> tuple[int, list[ChatSessionListItemVo]]:
        sql = ChatSessionModel.select().where(
            ChatSessionModel.is_deleted == 0
        ).offset(
            (dto.pagenum - 1) * dto.pagesize
        ).limit(
            dto.pagesize
        ).order_by(
            ChatSessionModel.gmt_motified.desc()
        )

        chat_session_list:list[ChatSessionModel] = await DBService.async_execute(sql)

        chat_session_vo_list:list[ChatSessionListItemVo] = [
            model_to_vo(item, ChatSessionListItemVo) # type: ignore
            for item in chat_session_list
        ]
        totol:int = len(chat_session_vo_list)

        return totol, chat_session_vo_list
