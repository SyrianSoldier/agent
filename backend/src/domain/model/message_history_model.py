import peewee
from .base_model import BaseModel, PeeweeFieldExtend
from enum import Enum

class ChatRole(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class MessageHistoryModel(BaseModel):
    parent_id:int = peewee.BigIntegerField(
        null=False,
        unique=True, # 形成的历史消息列表为单链表, 不存在两个节点的父节点相同的情况
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

    session_id:int = peewee.BigIntegerField(
        null=False,
        verbose_name="关联的会话id"
    )



    class Meta:
        table_name="message_history"
