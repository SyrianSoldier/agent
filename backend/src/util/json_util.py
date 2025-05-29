from typing import Any
import json
import enum
from src.util.validate_util import ValidateUtil
from playhouse.shortcuts import model_to_dict

class JsonUtil:
    @classmethod
    def dumps(cls, obj:object) -> str:
        def convert_obj(obj:Any) -> Any:
            if ValidateUtil.is_peewee_model(obj):
                return model_to_dict(obj)

            if isinstance(obj, enum.Enum):
                return obj.value

            raise TypeError(f"不支持序列化的类型:{obj}")


        return json.dumps(obj,default=convert_obj, ensure_ascii=False)

    @classmethod
    def loads(cls, s:str) -> Any:
        return json.loads(s)
