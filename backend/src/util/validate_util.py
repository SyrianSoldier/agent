from typing import TypeIs, Any
import inspect
import peewee
import dataclasses

class ValidateUtil:
    @classmethod
    def is_user_defined_class(cls, clazz: type) -> TypeIs[type[object]]:
        return inspect.isclass(clazz) and clazz.__module__ != "builtins"

    @classmethod
    def is_user_defined_class_ins(cls, obj: object) -> TypeIs[object]:
        return inspect.isclass(obj.__class__) and obj.__class__.__module__ != "builtins"

    @classmethod
    def is_dict_class(cls, clazz: type) ->  TypeIs[type[dict[Any,Any]]]:
        return inspect.isclass(clazz) and issubclass(clazz, dict)


    @classmethod
    def is_dict(cls, obj: object) -> TypeIs[dict[Any, Any]]:
        return isinstance(obj, dict)


    @classmethod
    def is_peewee_model_class(cls, clazz: type) -> TypeIs[type[peewee.Model]]:
        return inspect.isclass(clazz) and issubclass(clazz, peewee.Model)


    @classmethod
    def is_peewee_model(cls, ins:object) -> TypeIs[peewee.Model]:
        return isinstance(ins, peewee.Model)


    @classmethod
    def is_dataclass(cls, obj: object) -> TypeIs[object]: # TODO: 返回值类型不对
        return isinstance(obj, object) and dataclasses.is_dataclass(obj)


    @classmethod
    def is_dataclass_class(cls, clazz: type) -> TypeIs[type[Any]]: # TODO: 返回值类型不对
        return inspect.isclass(clazz) and dataclasses.is_dataclass(clazz)


    @classmethod
    def is_protected_key(cls, key:str) -> bool:
        return key.startswith("__") and key.endswith("__")


    @classmethod
    def is_private_key(cls, key:str) -> bool:
        return key.startswith("__")


    @classmethod
    def is_magic_key(cls, key:str) -> bool:
        return key.startswith("__") and key.endswith("__")


    @classmethod
    def is_public_key(cls, key:str) -> bool:
        return not (
            cls.is_private_key(key) or
            cls.is_protected_key(key) or
            cls.is_magic_key(key)
        )
