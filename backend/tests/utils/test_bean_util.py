import pytest
from src.domain.vo.base_vo import BaseVo
from src.util.bean_util import BeanUtil
from src.domain.dto.base_dto import BaseDto
from src.domain.model.base_model import BaseModel
import peewee as pw
from typing import Any
import unittest
import datetime
from dataclasses import dataclass, field
from enum import Enum

class TestBeanUtil(unittest.TestCase):
    """python -m pytest tests/utils/test_bean_util.py::TestBeanUtil
    """

    def test_from_dict_to_class(self) -> None:
        """测试从字典转换为类实例"""
        class Person:
            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

        person_dict: dict[str, Any] = {"name": "Alice", "age": 25, "gender": "female"}
        person = BeanUtil.to_bean(person_dict, Person, name="", age="")

        assert person.name == "Alice"
        assert person.age == 25
        try:
            # gender 不在 Person 类中，应该抛出 AttributeError
            person.gender   # type: ignore
        except AttributeError:
            pass


    def test_from_class_to_dict(self) -> None:
        """测试从类实例转换为字典"""
        class Car:
            def __init__(self, brand: str, model: str) -> None:
                self.brand = brand
                self.model = model

        car_obj = Car(brand="Toyota", model="Corolla")
        car_dict: dict[str, Any] = BeanUtil.to_bean(car_obj, dict)
        self.assertDictEqual(car_dict,  {"brand": "Toyota", "model": "Corolla"})


    def test_from_dict_to_dict(self) -> None:
        """测试从字典转换为字典"""
        source_dict: dict[str, Any] = {"name": "Bob", "age": 30, "_private": "secret", "__init__": "method"}
        target_dict: dict[str, Any] = {"name": ""}
        merged_dict:dict[str, Any] = BeanUtil.to_bean(source_dict, target_dict)

        self.assertDictEqual(merged_dict,  {"name": "Bob"})


    def test_deep_clone_enabled(self) -> None:
        """测试深拷贝功能"""
        source_dict: dict[str, Any] = {"name": "Bob", "age": 30, "friend": {"name": "ZS"}}
        target_dict: dict[str, Any] = {"name": "", "friend": None}
        merged_dict:dict[str, Any] = BeanUtil.to_bean(source_dict, target_dict, deep_clone=True)


        self.assertDictEqual(merged_dict, {"name": "Bob", "friend": {"name": "ZS"}})

        source_dict["friend"]["name"] = "LISI"
        self.assertTrue(merged_dict["friend"]["name"] == "ZS")


    def test_deep_clone_disabled(self) -> None:
        """测试禁用深拷贝功能"""
        source_dict: dict[str, Any] = {"name": "Bob", "age": 30, "friend": {"name": "ZS"}}
        target_dict: dict[str, Any] = {"name": "", "friend": None}
        merged_dict:dict[str, Any] = BeanUtil.to_bean(source_dict, target_dict)


        self.assertDictEqual(merged_dict, {"name": "Bob", "friend": {"name": "ZS"}})

        source_dict["friend"]["name"] = "LISI"
        self.assertTrue(merged_dict["friend"]["name"] == "LISI")


    def test_from_dict_with_special_keys(self) -> None:
        """测试字典中含有特殊键（魔术方法、私有属性、受保护属性）的情况"""
        source_dict: dict[str, Any] = {
            "name": "Bob",
            "age": 30,
            "_private": "secret",
            "__init__": "method"
        }
        target_dict: dict[str, Any] = {"name": "", "age": 0}
        merged_dict:dict[str, Any] = BeanUtil.to_bean(source_dict, target_dict)

        self.assertDictEqual(merged_dict, {"name": "Bob", "age": 30})


    def test_invalid_from_type(self) -> None:
        """测试当from_和to参数不是字典或对象实例时抛出 TypeError"""
        with pytest.raises(TypeError):
             BeanUtil.to_bean("invalid_type", dict)

        with pytest.raises(TypeError):
            BeanUtil.to_bean({}, "invalid_type") # type: ignore


    def test_from_object_to_class(self) -> None:
        """测试从对象实例转换为类实例"""
        class Car:
            def __init__(self, brand: str, model: str) -> None:
                self.brand = brand
                self.model = model

        car_obj = Car(brand="Toyota", model="Corolla")
        car_instance: Car = BeanUtil.to_bean(car_obj, Car, brand="", model="")

        assert isinstance(car_instance, Car)
        assert car_instance.brand == "Toyota"
        assert car_instance.model == "Corolla"


    def test_from_dict_with_default_value(self) -> None:
        """测试当from_字典中缺少某些目标类属性时，是否使用默认值"""
        class Person:
            def __init__(self, name: str, age: int = 20) -> None:
                self.name = name
                self.age = age

        person_dict: dict[str, Any] = {"name": "Alice"}
        person: Person = BeanUtil.to_bean(person_dict, Person, name=None)

        assert person.name == "Alice"
        assert person.age == 20



    def test_object_to_dict_with_empty_dict(self) -> None:
        """测试从对象实例转换为空字典的场景"""
        class Item:
            def __init__(self, id: int, name: str) -> None:
                self.id = id
                self.name = name

        item_obj = Item(id=1, name="Item1")
        item_dict: dict[str, Any] = BeanUtil.to_bean(item_obj, dict)

        self.assertDictEqual(item_dict, {"id": 1, "name": "Item1"})


    def test_request_body_to_dto(self) -> None:
        request_data = {
            "username": "john",
            "email": "john@example.com",
            "signup_time": "2023-01-01T12:00:00",

            # 前端可能传超量的数据
            "other1": "xxxx",
            "other2": "xxxx",
            "other3": "xxxx",
            "other4": "xxxx",
            "other5": "xxxx"
        }
        @dataclass
        class UserCreateDto():
            username: str|None = None
            email: str | None = None
            age: int = 18
            signup_time: str|None = None

            extra:str|None = None


        dto = BeanUtil.to_bean(request_data, UserCreateDto)

        self.assertIsInstance(dto, UserCreateDto)
        self.assertEqual(dto.username, "john")
        self.assertEqual(dto.email, "john@example.com")
        self.assertEqual(dto.age, 18)  # 测试默认值
        self.assertEqual(dto.signup_time, "2023-01-01T12:00:00")
        self.assertEqual(dto.extra, None)


    def test_dto_to_model(self) -> None:
        @dataclass
        class UserCreateDto():
            username:str | None = field(default=None)
            email:str | None = field(default=None)
            other:dict[str, Any] = field(default_factory=dict)


        class UserModel(BaseModel):
            username:str = pw.CharField()
            email = pw.CharField()
            age = pw.IntegerField(default=18)
            signup_time = pw.DateTimeField()

            def __str__(self) -> str:
                return "UserModel(xxx)"

        dto = UserCreateDto(
            username="alice",
            email="alice@example.com"
        )
        assert dto.username == "alice"
        assert dto.email == "alice@example.com"
        self.assertDictEqual(dto.other, {})

        model = BeanUtil.to_bean(dto, UserModel)

        assert model.username == "alice"
        assert model.email == "alice@example.com"
        assert model.age == 18
        assert model.signup_time == None


    def test_model_to_vo(self) -> None:
        class UserModel(BaseModel):
            username = pw.CharField()
            email = pw.CharField()
            age = pw.IntegerField(null=True, default=18)
            signup_time = pw.DateTimeField()

        @dataclass
        class UserVo(BaseVo):
            username: str|None = None
            age: int|None = None

        model = UserModel(
            username="bob",
            email="bob@example.com",
            signup_time="2023-01-01T12:00:00"
        )

        self.assertEqual(model.id, None)
        self.assertEqual(model.is_deleted, 0)
        self.assertEqual(model.username, "bob")
        self.assertEqual(model.signup_time, "2023-01-01T12:00:00")
        self.assertEqual(model.id, None)

        vo = BeanUtil.to_bean(model, UserVo)

        self.assertEqual(vo.username, "bob")
        self.assertEqual(vo.age, 18)


    def test_vo_to_request_body(self) -> None:

        @dataclass
        class UserVo:
            username: str
            age: int
            friend_address:str = "hunan"

        vo = UserVo(username="zs", age=18)

        obj = BeanUtil.to_bean(vo, dict)

        assert obj["username"] == "zs"
        assert obj["age"] == 18
        assert obj["friend_address"] == "hunan"

    def test_set_attr(self) -> None:
        class Status(Enum):
              ACTIVE = "active"
              DEACTIE = "deactive"

        @dataclass
        class Test():
            a:Status|None = None
            b:str|None = None

        obj = Test()

        BeanUtil.set_attr(obj, "a", "active", convert=True) # 自动转成了Status.Avtive
        assert obj.a is Status.ACTIVE

        BeanUtil.set_attr(obj, "a", None, convert=True)
        assert obj.a is None

        # 无法映射的属性值,会被忽略直接赋值
        BeanUtil.set_attr(obj, "a", "无法映射的属性值", convert=True)
        assert obj.a == "无法映射的属性值"

        BeanUtil.set_attr(obj, "b", "一段字符串", convert=True)
        assert obj.b == "一段字符串"


