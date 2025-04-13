from peewee import SQL, DateTimeField
import peewee_async
from typing_extensions import Dict, Any
from src.util.env_util import EnvUtil

db_config:Dict[str, Any] = EnvUtil.get_cur_env_config().get("database") #type:ignore[assignment]
db = peewee_async.PooledMySQLDatabase(**db_config)


class BaseModel(peewee_async.AioModel): #type:ignore[misc]
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(
        constraints=[
            SQL("DEFAULT CURRENT_TIMESTAMP"),
            SQL("ON UPDATE CURRENT_TIMESTAMP"),
        ]
    )

    class Meta:
        database = db
