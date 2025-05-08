from .base_dto import BaseDto, PaginationDto
from pydantic import Field
from typing import Annotated

class ChatSessionCreateDto(BaseDto):
    title: Annotated[str, Field(min_length=1, max_length=100)]


class ChatSessionDeleteDto(BaseDto):
    uuid: str


class ChatSessionRenameDto(BaseDto):
    uuid: str
    title: Annotated[str, Field(min_length=1, max_length=100)]


class ChatSessionDetailDto(BaseDto):
    uuid: str


class ChatSessionListDto(PaginationDto):
    pass
