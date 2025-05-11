from typing import Any

import peewee
from enum import Enum
from peewee import SQL
import peewee_async
from src.util.env_util import EnvUtil
from src.util.bean_util import BeanUtil
import re
from src.util.time_util import TimeUtil

# peewee的字段和数据库字段对照表:
#   - https://docs.peewee-orm.com/en/latest/peewee/models.html#field-types-table

# peewee字段扩展文档:
#   - https://docs.peewee-orm.com/en/latest/peewee/models.html#custom-fields

# peewee所有字段的通用属性
#   - https://docs.peewee-orm.com/en/latest/peewee/models.html#field-initialization-arguments

# peewee某些字段的单独属性
#   - https://docs.peewee-orm.com/en/latest/peewee/models.html#some-fields-take-special-parameters


db_config:dict[str, Any] = EnvUtil.get_cur_env_config().get("database") #type:ignore
db = peewee_async.PooledMySQLDatabase(**db_config)


class PeeweeFieldExtend():
    class TinyIntField(peewee.IntegerField): #type:ignore
        field_type:str = "TINYINT UNSIGNED"


    class EnumField(peewee.Field): #type:ignore
        field_type:str = "VARCHAR(100)"

        def __init__(self, enum_class: type[Enum], *args:Any, **kwargs:Any):
            self.enum_clss = enum_class
            super().__init__(*args, **kwargs)


        def python_value(self, db_value: str | None) -> Enum | None :
            return self.enum_clss._value2member_map_.get(db_value, None) if db_value is not None else None


        def db_value(self, python_value: Enum | None) -> str | None:
            return python_value.value if python_value is not None else None


    class DateTime6Field(peewee.TextField): #type:ignore
        """1. peewee.datetime 反序列化时会自动将时间转为datetime对象, 不想用这个功能, 所以自定义一个字段
           此时项目中所有从数据库读下来的时间都会是字符串
           2. 精确到6微秒存储
        """
        field_type:str = "DATETIME(6)"




class BaseModel(peewee_async.AioModel): #type:ignore[misc]
    """peewee作者非常反感类型注解, 坚决反对,所以peewee没有类型注解, 从2018年到2024依旧如此"
       peewee的Model可以直接实例化, 字段默认值是None
    """
    id = peewee.BigIntegerField(
        primary_key=True,
        null=False,
        constraints=[SQL("AUTO_INCREMENT")],
    )

    is_deleted = PeeweeFieldExtend.TinyIntField(
        null=False,
        default=0,
        verbose_name="是否被删除, 0未删除,1已删除",
    )

    gmt_create = PeeweeFieldExtend.DateTime6Field(
        null=False,
        default=lambda: TimeUtil.now_utc(),
        # constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")],
        # formats=TimeUtil.default_time_format,
        verbose_name="创建时间"
    )

    gmt_modified = PeeweeFieldExtend.DateTime6Field(
        null=False,
        default=lambda: TimeUtil.now_utc(),
        # constraints=[SQL("DEFAULT CURRENT_TIMESTAMP"), SQL("ON UPDATE CURRENT_TIMESTAMP")],
        # formats=TimeUtil.default_time_format,
        verbose_name="更新时间"
    )

    class Meta:
        database = db
        # 子表应该实现table_name, 团队约定:必须用snake_case风格
        # table_name = "base_model"

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        model_name:str = self.__class__.__name__
        field_names:list[str] = list(self.__class__._meta.sorted_field_names) # pylint: disable=no-member
        filed_strs:list[str] = []
        repr_str = f"{model_name}(placeholder)" # Model(a=1,b=2,c=2)

        for key in field_names:
            value:str = str(BeanUtil.get_value(self, key))
            filed_strs.append(f"{key}={value}")

        return re.sub(r"placeholder", ",".join(filed_strs), repr_str)
