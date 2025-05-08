from typing_extensions import override
from .base_service import BaseService
from src.service.log_service import LogService
from src.domain.model.chat_session_model import ChatSessionModel
from src.service.db_service import DBService
from src.domain.vo.chat_session_vo import ChatSessionVo
from src.domain.vo.base_vo import PaginationVo
from src.domain.dto.chat_session_dto import ChatSessionCreateDto, ChatSessionDeleteDto, ChatSessionRenameDto, ChatSessionDetailDto
from src.domain.dto.base_dto import PaginationDto
from src.util.bean_util import BeanUtil

class ChatSeesionService(BaseService):
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
    async def create_chat_session(cls, dto: ChatSessionCreateDto) -> ChatSessionVo:
        model = BeanUtil.to_bean(dto, ChatSessionModel)
        model.create_user = 0 # TODO: 添加user
        await DBService.async_insert(model)
        return BeanUtil.to_bean(model, ChatSessionVo)



    @classmethod
    async def delete_chat_session(cls, dto: ChatSessionDeleteDto) -> None:
        sql = ChatSessionModel.update(is_deleted=1).where(
            (ChatSessionModel.uuid == dto.uuid) &
            (ChatSessionModel.is_deleted == 0)
        )

        await DBService.async_logic_delete(sql)


    @classmethod
    async def rename_chat_session_title(cls, dto:ChatSessionRenameDto) -> None:
        sql = ChatSessionModel.update(
            title = dto.title
        ).where(
            (ChatSessionModel.uuid == dto.uuid) &
            (ChatSessionModel.is_deleted  == 0)
        )


        await DBService.async_update(sql)


    @classmethod
    async def get_chat_session_list(cls, dto: PaginationDto) -> PaginationVo:
        sql = ChatSessionModel.select().where(
            ChatSessionModel.is_deleted == 0
        ).offset(
            (dto.pagenum - 1) * dto.pagesize
        ).limit(
            dto.pagesize
        ).order_by(
            ChatSessionModel.gmt_modified.desc()
        )

        chat_session_list:list[ChatSessionModel] = await DBService.async_query_list(sql)

        chat_session_vo_list:list[ChatSessionVo] = [
            BeanUtil.to_bean(item, ChatSessionVo)
            for item in chat_session_list
        ]

        totol:int = len(chat_session_vo_list)

        vo = PaginationVo(total=totol, list=chat_session_list)
        return vo


    @classmethod
    async def get_chat_session_detail(cls, dto: ChatSessionDetailDto) -> ChatSessionVo:
        sql = ChatSessionModel.select().where(
            (ChatSessionModel.is_deleted == 0) &
            (ChatSessionModel.uuid == dto.uuid)
        )

        model = await DBService.async_query_detail(sql)
        # TODO: 处理model为none的情况
        vo = BeanUtil.to_bean(model, ChatSessionVo)
        return vo
