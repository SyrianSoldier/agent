from typing_extensions import override

from src.util.time_util import TimeUtil
from .base_service import BaseService
from src.service.log_service import LogService
from src.domain.model.chat_session_model import ChatSessionModel
from src.service.db_service import DBService
from src.domain.vo.chat_session_vo import ChatSessionVo
from src.domain.vo.base_vo import PaginationVo
from src.domain.dto.chat_session_dto import ChatSessionCreateDto, ChatSessionDeleteDto, ChatSessionRenameDto, ChatSessionDetailDto
from src.domain.dto.base_dto import PaginationDto
from src.util.bean_util import BeanUtil

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



    @classmethod
    async def get_chat_session_list(cls, dto: PaginationDto) -> PaginationVo:
        base_sql = ChatSessionModel.select().where(
            ChatSessionModel.is_deleted == 0
        )

        list_sql = base_sql.offset(
            (dto.pagenum - 1) * dto.pagesize
        ).limit(
            dto.pagesize
        ).order_by(
            ChatSessionModel.id.desc()
        )

        chat_session_list:list[ChatSessionModel] = await DBService.async_query_list(list_sql)

        chat_session_vo_list:list[ChatSessionVo] = [
            BeanUtil.to_bean(item, ChatSessionVo)
            for item in chat_session_list
        ]

        totol:int = base_sql.count()

        vo = PaginationVo(total=totol, list=chat_session_vo_list)
        return vo



