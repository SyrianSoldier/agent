from .base_dto import BaseDto
from pydantic import Field
from typing import Annotated

class ChatSessionCreateDto(BaseDto):
    title: Annotated[str, Field(min_length=1, max_length=30)]
    user_id: Annotated[int, Field(gt=0)]


class ChatSessionDeleteDto(BaseDto):
    uuid: Annotated[int, Field(ge=1)]


class ChatSessionRenameDto(BaseDto):
    uuid: Annotated[int, Field(ge=1)]
    title: Annotated[str, Field(min_length=1, max_length=30)]
