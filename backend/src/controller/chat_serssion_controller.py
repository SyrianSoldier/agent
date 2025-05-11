from .base_controller import BaseController
from src.service.chat_serssion_service import ChatSeesionService
from src.domain.dto.chat_session_dto import (
    ChatSessionCreateDto,
    ChatSessionDeleteDto,
    ChatSessionRenameDto,
    ChatSessionDetailDto,
    ChatSessionListDto,
)

class Create(BaseController):
    async def post(self) -> None:
        dto = self.request_body_to_dto(ChatSessionCreateDto)
        vo = await ChatSeesionService.create_chat_session(dto)
        self.return_success(data=vo)


class Delete(BaseController):
    async def post(self) -> None:
        dto = self.request_body_to_dto(ChatSessionDeleteDto)
        await ChatSeesionService.delete_chat_session(dto)
        self.return_success()


class Rename(BaseController):
    async def post(self) -> None:
        dto = self.request_body_to_dto(ChatSessionRenameDto)
        await ChatSeesionService.rename_chat_session_title(dto)
        self.return_success()


class Detail(BaseController):
    async def get(self) -> None:
        dto = self.request_body_to_dto(ChatSessionDetailDto)
        vo = await ChatSeesionService.get_chat_session_detail(dto)
        self.return_success(data=vo)



class List(BaseController):
    async def get(self) -> None:
        dto = self.request_body_to_dto(ChatSessionListDto)
        vo = await ChatSeesionService.get_chat_session_list(dto)
        self.return_success(data=vo)
