from .base_vo import BaseVo
from dataclasses import dataclass

@dataclass
class ChatSessionVo(BaseVo):
    create_at:str|None = None
    modified_at:str|None = None
    title:str|None = None
    uuid:str|None = None

