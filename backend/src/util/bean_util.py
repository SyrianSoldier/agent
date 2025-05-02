import inspect
import copy
from typing import Any


class BeanUtil:

    @classmethod
    def to_bean[T, U](cls, from_: T, to: type[U], deep_clone: bool = False) -> U:
        """
        将 `from_` 的键值对映射到 `to` 类型的实例。

        该函数接受一个字典或对象 `from_`，并根据 `from_` 和 `to` 之间的属性交集构造 `to` 类型的实例。它会自动忽略魔术方法、私有属性和受保护属性，确保映射的属性是公开可用的。

        注意：
        - 如果 `to` 是一个类，则会创建该类的实例。
        - 如果 `to` 是一个类, 则from中必须包含能让to初始化的key-value(可以没有含默认值的参数)
        - 如果 `to` 是一个字典类型，则返回一个字典，其中包含与 `from_` 属性交集的键值对。
        - 如果 `from_` 和 `to` 之间有不匹配的属性，将会被忽略。

        Args:
            from_ (T): 源对象，可以是字典或对象实例。
            to (type[U]): 目标类型, 可以是类或dict(类)。
            deep_clone(bool): 是否以深克隆的方式将from中的属性复制到to.

        Returns:
            U: `to` 类型的实例或字典，包含来自 `from_` 的值。

        Raises:
            TypeError: 如果 `from_` 不是字典或对象实例，或者 `to` 既不是类也不是字典类型。

        Example:
            # 示例 1: 从字典转换为类实例
            >>> class Person:
            >>>     def __init__(self, name, age):
            >>>         self.name = name
            >>>         self.age = age
            >>> person_dict = {"name": "Alice", "age": 25, "gender": "female"}
            >>> person = to_bean(person_dict, Person)
            >>> print(person.name, person.age)  # 输出: Alice 25
            >>> print(person.gender)  # 会抛出 AttributeError，因为 "gender" 不在目标类属性中

            # 示例 2: 从对象实例转换为类实例
            >>> class Car:
            >>>     def __init__(self, brand, model):
            >>>         self.brand = brand
            >>>         self.model = model
            >>> car_obj = Car(brand="Toyota", model="Corolla")
            >>> car_dict = to_bean(car_obj, dict)
            >>> print(car_dict)  # 输出: {'brand': 'Toyota', 'model': 'Corolla'}

            # 示例 3: 从字典转换为字典
            >>> source_dict = {"name": "Bob", "age": 30, "_private": "secret", "__init__": "method"}
            >>> target_dict = {"name": "", "age": 0}
            >>> merged_dict = to_bean(source_dict, target_dict)
            >>> print(merged_dict)  # 输出: {'name': 'Bob', 'age': 30}
        """

        def is_special_key(key: str) -> bool:
            # 魔术方法，如 __init__, __str__ 等
            if key.startswith("__") and key.endswith("__"):
                return True

            # 私有属性，如 __password
            if key.startswith("__"):
                return True

            # 受保护属性，如 _name
            if key.startswith("_"):
                return True

            return False


        def is_user_defined_class(cls: type) -> bool:
            return inspect.isclass(cls) and cls.__module__ != "builtins"


        def is_dict_class(cls: type) -> bool:
            return inspect.isclass(cls) and issubclass(cls, dict)


        def get_value(
            obj: dict[str, Any] | object, key: str, default: Any = None
        ) -> Any:
            """统一获取对象/实例值的方式，并返回深拷贝副本，避免外部修改原值"""
            value = None

            if isinstance(obj, dict):
                value = obj.get(key, default)
            elif isinstance(obj, object):
                value = getattr(obj, key, default)
            else:
                raise TypeError(
                    "The 'obj' parameter must be either a dictionary or an object instance."
                )

            return copy.deepcopy(value) if deep_clone else value


        def get_from_keys() -> set[str]:
            if isinstance(from_, dict):
                return {key for key in from_.keys() if not is_special_key(key)}

            if isinstance(from_, object) and hasattr(from_, "__dict__"):
                return {key for key in from_.__dict__.keys() if not is_special_key(key)}

            raise TypeError(
                "The 'from_' parameter must be either a dictionary or an object instance."
            )


        def get_to_keys() -> set[str]:
            """to支持 dict, {}, 两种方式"""
            if is_user_defined_class(to) or is_dict_class(to):
                return get_from_keys()

            if isinstance(to, dict):
                return {key for key in to.keys() if not is_special_key(key)}

            raise TypeError("Parameter 'to' must be a class or a dict instance.")


        def create_to_instance() -> U:
            """根据from和to属性的交集构造to的实例"""
            from_to_intersection: set[str] = get_from_keys() & get_to_keys()

            if is_user_defined_class(to) or is_dict_class(to):
                return to(
                    **{key: get_value(from_, key) for key in from_to_intersection}
                )

            if isinstance(to, dict):
                to_deep_copy: dict[str, Any] = copy.deepcopy(to)

                return {
                    **to_deep_copy,
                    **{key: get_value(from_, key) for key in from_to_intersection},
                }

            raise TypeError("Parameter 'to' must be a class or a dict instance.")

        return create_to_instance()
