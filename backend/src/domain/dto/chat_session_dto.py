from .base_dto import BaseDto, PaginationDto
from dataclasses import dataclass

@dataclass
class ChatSessionCreateDto(BaseDto):
    title: str|None = None

@dataclass
class ChatSessionDeleteDto(BaseDto):
    uuid: str|None = None

@dataclass
class ChatSessionRenameDto(BaseDto):
    uuid: str|None = None
    title: str|None = None

@dataclass
class ChatSessionDetailDto(BaseDto):
    uuid: str|None = None

@dataclass
class ChatSessionListDto(PaginationDto):
    pass
