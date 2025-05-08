import copy
import dataclasses

from typing import Any
from .validate_util import ValidateUtil


class BeanUtil:
    @classmethod
    def get_value(
        cls,
        obj: dict[str, Any] | object,
        key: str,
        *,
        default: Any = None,
        deep_clone: bool = False
    ) -> Any:
        """统一获取对象/实例值的方式，并可选择返回深拷贝副本，避免外部修改原值"""

        def get_item_value(
            obj: dict[str, Any] | object,
            *,
            key: str,
            default: Any = None,
        ) -> Any:
            if ValidateUtil.is_dict(obj):
                return obj.get(key, default)

            if ValidateUtil.is_user_defined_class_ins(obj):
                return getattr(obj, key, default)

            raise TypeError(
                "The 'obj' parameter must be either a dictionary or an object instance."
            )

        if key.strip() == "":
            raise TypeError(
                "The key is invalid beacause it shounld't be an empty string."
            )

        keys:list[str] = key.split(".") # "a.b.c" --> ["a","b","c"]
        default = copy.deepcopy(default) # 拷贝一份default
        value = obj

        for k in keys:
            value = get_item_value(
                value,
                key=k,
                default=None,
            )

            if value is None:
                return default


        return copy.deepcopy(value) if deep_clone else value


    @classmethod
    def get_obj_keys(cls, obj: object) -> set[str]:
        """获取实例/字典的key的方法, 排除私有,保护属性,魔术属性"""
        if ValidateUtil.is_dict(obj):
            return {
                key
                for key in obj.keys()
                if ValidateUtil.is_public_key(key)
            }

        if ValidateUtil.is_dataclass(obj):
            return {
                field.name
                for field in dataclasses.fields(obj) # type:ignore
            }

        if ValidateUtil.is_peewee_model(obj):
            # peewee的原始数据(即实例化时的数据)放在__dict__.__data__里
            origin_data_dict: dict[str, Any] = cls.get_value(
                obj,
                key="__dict__.__data__",
                default={},
                deep_clone=True
            )


            return {
                key
                for key in origin_data_dict.keys()
                if ValidateUtil.is_public_key(key)
            }

        # 普通python对象
        if isinstance(obj, object) and hasattr(obj, "__dict__"):
            return {
                key
                for key in obj.__dict__.keys()
                if ValidateUtil.is_public_key(key)
            }

        raise TypeError(
            "The 'obj'  must be either a dictionary or an object instance."
        )


    @classmethod
    def new_instance(
        cls,
        clazz: type[object],
        *args: Any,
        **kwargs: Any
    ) -> object:
        """
        安全创建实例的工厂方法：
        1. 优先尝试无参默认构造
        2. 失败后尝试使用传入的 *args 和 **kwargs 构造
        3. 全部失败时抛出 InstanceCreationError
        """
        first_error, second_error = None, None

        # 优先尝试无参构造
        try:
            return clazz()
        except Exception as e:
            first_error = e

        # 无参构造失败后，尝试带参构造
        try:
            return clazz(*args, **kwargs)
        except Exception as e:
            second_error = e

        # 聚合错误信息
        error_msg = (
            f"Failed to create instance of {clazz.__name__!r}.\n"
            f"Attempt 1 (default constructor): {type(first_error).__name__}: {first_error}\n"
            f"Attempt 2 (with parameters): {type(second_error).__name__}: {second_error}"
        )
        raise ValueError(error_msg) from second_error



    @classmethod
    def to_bean[T, U](
        cls,
        from_: T,
        to: type[U],
        deep_clone: bool = False,
        *init_to_args: Any,
        **init_to_kwargs: Any
    ) -> U:
        """
        功能:
        1. **功能**: 将 `from_` 的键值对映射到 `to` 类型的实例。
        2. 该函数接受一个字典或对象(实例)`from_`，并根据 `from_` 和 `to` 之间的属性交集构造 `to` 类型的实例。
        3. 它会自动忽略魔术方法、私有属性和受保护属性，确保映射的属性是公开可用的。

        注意：
        - 如果 `to` 是一个类, 则必须保证创建实例时不包含参数(无参构造), 否则需要通过`init_to_args`, `init_to_kwargs`将构造函数的参数传递进来进行实例化

        Args:
            from_ (T): 源对象，可以是字典或对象实例。
            to (type[U]): 目标类型, 目前支持 `普通python class`、`dict`、`字典字面量`。
            deep_clone(bool): 是否以深克隆的方式将from中的属性复制到to, 默认值为false

        Returns:
            U: `to` 类型的实例或字典，包含来自 `from_` 的值。

        Example:
            可参考 tests/utils/test_bean_util.py
        """
        from_keys = cls.get_obj_keys(from_)
        to_keys: set[str] | None = None
        to_ins: U | None = None

        if ValidateUtil.is_dict_class(to):
            to_keys = set()

        elif ValidateUtil.is_dict(to):
            to_keys = cls.get_obj_keys(to)

        elif ValidateUtil.is_user_defined_class(to):
            to_ins = cls.new_instance(to, *init_to_args, **init_to_kwargs) # type:ignore

            if ValidateUtil.is_peewee_model_class(to):
                to_keys = set(to._meta.fields.keys())
            else:
                to_keys = cls.get_obj_keys(to_ins)


        else:
            raise TypeError("Parameter 'to' must be an instance of a user-defined class or a dict class or a dictionary.")

        keys_intersection:set[str] = from_keys & to_keys


        if ValidateUtil.is_dict(to):
            to_deep_copy: dict[str, Any] = copy.deepcopy(to)

            update_dict: dict[str, Any] = {
                key: cls.get_value(from_, key, deep_clone=deep_clone)
                for key in keys_intersection
            }

            return {
                **to_deep_copy,
                **update_dict,
            }

        if ValidateUtil.is_dict_class(to):
            return {
                key: cls.get_value(from_, key, deep_clone=deep_clone)
                for key in from_keys
            }

        elif ValidateUtil.is_user_defined_class(to) and (to_ins is not None):
            for key in keys_intersection:
                setattr(to_ins, key, cls.get_value(from_, key, deep_clone=deep_clone))
            return to_ins

        raise TypeError("Parameter 'to' must be an instance of a user-defined class or a dict class or a dictionary.")
