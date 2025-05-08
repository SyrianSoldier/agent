from .base_vo import BaseVo
from dataclasses import dataclass

@dataclass
class ChatSessionVo(BaseVo):
    gmt_create:str
    gmt_modified:str
    title:str
    uuid:str



