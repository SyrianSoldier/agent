import uuid
from peewee import CharField, BigIntegerField
from .base_model import BaseModel


class SessionModel(BaseModel):
    session_uid: str = CharField(primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id:int = BigIntegerField(index=True, null=False)

    class Meta:
        table_name:str = "session"
        # TODO: 什么是索引
        # indexes = (
        #     # 复合索引：快速查询活跃会话
        #     (('user_id', 'expires_at', 'is_revoked'), False),
        # )


