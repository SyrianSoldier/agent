from typing import Any

import peewee
from peewee import SQL
import peewee_async
from src.util.env_util import EnvUtil

db_config:dict[str, Any] = EnvUtil.get_cur_env_config().get("database") #type:ignore[assignment]
db = peewee_async.PooledMySQLDatabase(**db_config)

class BaseModel(peewee_async.AioModel): #type:ignore[misc]
    created_at = peewee.DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = peewee.DateTimeField(
        constraints=[
            SQL("DEFAULT CURRENT_TIMESTAMP"),
            SQL("ON UPDATE CURRENT_TIMESTAMP"),
        ]
    )

    class Meta:
        database = db
