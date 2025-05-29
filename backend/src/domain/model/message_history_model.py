import peewee
from .base_model import BaseModel, PeeweeFieldExtend
from enum import Enum

class ChatRole(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class MessageHistoryModel(BaseModel):
    parent_id:str = peewee.BigIntegerField(
        null=False, # parent_id为预留字段,暂时不用
        default=-1,
        verbose_name="上一条历史消息的id"
    )

    content:str = peewee.TextField(
        null=False,
        verbose_name="历史消息内容"
    )

    thinking_content:str = peewee.TextField(
        null=True,
        verbose_name="深度思考的消息内容"
    )

    role:ChatRole = PeeweeFieldExtend.EnumField(
        enum_class=ChatRole,
        null=False,
        verbose_name="聊天角色"
    )

    session_uuid:str = peewee.CharField(
        null=False,
        max_length=256,
        verbose_name="关联的会话id"
    )



    class Meta:
        table_name="message_history"

    def __repr__(self) -> str:
        return super().__repr__()
