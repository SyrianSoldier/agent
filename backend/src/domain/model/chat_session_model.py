import peewee
import uuid
from .base_model import BaseModel

class ChatSessionModel(BaseModel):
    title:str = peewee.CharField(
        max_length=100,
        null=False,
        verbose_name="会话标题"
    )

    create_user:int = peewee.BigIntegerField(
        null=False,
        verbose_name="创建seesion的用户"
    )

    uuid:str = peewee.CharField(
        max_length=40,
        null=False,
        unique=True,
        default=lambda: uuid.uuid4().hex,
        verbose_name="会话唯一uuid"
    )

    class Meta:
        table_name="chat_session"

    def __repr__(self) -> str:
        return super().__repr__()
