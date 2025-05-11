import peewee
from .base_model import BaseModel


class UserModel(BaseModel):
    username:str = peewee.CharField(
        max_length=50,
        null=False,
        unique=True,
        verbose_name="用户名",
    )

    phone_numer:str= peewee.CharField(
        max_length=20,
        null=False,
        unique=True,
        verbose_name="手机号",
    )


    class Meta:
        table_name="user"

    def __repr__(self) -> str:
        return super().__repr__()
