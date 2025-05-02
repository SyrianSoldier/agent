from src.util.bean_util import BeanUtil
from src.domain.dto.base_dto import BaseDto
from src.domain.model.base_model import BaseModel
import peewee as pw
from typing import Any
import unittest
import datetime
from dataclasses import dataclass



class TestBeanUtil(unittest.TestCase):
    def test_from_dict_to_class(self) -> None:
        """测试从字典转换为类实例"""
        class Person:
            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

        person_dict: dict[str, Any] = {"name": "Alice", "age": 25, "gender": "female"}
        person = BeanUtil.to_bean(person_dict, Person)

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
        """测试当from_参数不是字典或对象实例时抛出 TypeError"""
        try:
            BeanUtil.to_bean("invalid_type", dict)
        except TypeError as e:
            assert str(e) == "The 'from_' parameter must be either a dictionary or an object instance."


    def test_invalid_to_type(self) -> None:
        """测试当to参数既不是类也不是字典类型时抛出 TypeError"""
        try:
            BeanUtil.to_bean({}, "invalid_type") # type: ignore
        except TypeError as e:
            assert str(e) == "Parameter 'to' must be a class or a dict instance."


    def test_from_object_to_class(self) -> None:
        """测试从对象实例转换为类实例"""
        class Car:
            def __init__(self, brand: str, model: str) -> None:
                self.brand = brand
                self.model = model

        car_obj = Car(brand="Toyota", model="Corolla")
        car_instance: Car = BeanUtil.to_bean(car_obj, Car)

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
        person: Person = BeanUtil.to_bean(person_dict, Person)

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
        class UserCreateDto(BaseDto):
            username: str
            email: str
            age: int = 18  # 默认值测试
            signup_time: str


        request_data = {
            "username": "john",
            "email": "john@example.com",
            "signup_time": "2023-01-01T12:00:00"
        }

        dto = BeanUtil.to_bean(request_data, UserCreateDto)

        self.assertIsInstance(dto, UserCreateDto)
        self.assertEqual(dto.username, "john")
        self.assertEqual(dto.age, 18)  # 测试默认值
        self.assertEqual(dto.signup_time, "2023-01-01T12:00:00")


    def test_dto_model(self) -> None:
        class UserCreateDto(BaseDto):
            username: str
            email: str
            age: int = 18  # 默认值测试
            signup_time: str


        # Peewee Model
        class UserModel(BaseModel):
            user_name = pw.CharField()  # 字段名不一致测试
            email = pw.CharField()
            age = pw.IntegerField(null=True)
            signup_time = pw.DateTimeField()

        # Dataclass VO
        @dataclass
        class UserVo:
            username: str
            email: str
            age: int
            signup_time: datetime.datetime

        dto = UserCreateDto(
            username="alice",
            email="alice@example.com",
            signup_time="2023-01-01T12:00:00"
        )

        # 测试字段名映射（username -> user_name, signup_time -> created_at）
        model = BeanUtil.to_bean(dto, UserModel)

        self.assertIsInstance(model, UserModel)
        self.assertEqual(model.user_name, "alice")
        self.assertEqual(model.signup_time, "2023-01-01T12:00:00")
        self.assertEqual(model.age, 18)


    def test_model_to_vo(self) -> None:
        class UserCreateDto(BaseDto):
            username: str
            email: str
            age: int = 18  # 默认值测试
            signup_time: str


        # Peewee Model
        class UserModel(BaseModel):
            user_name = pw.CharField()  # 字段名不一致测试
            email = pw.CharField()
            age = pw.IntegerField(null=True)
            signup_time = pw.DateTimeField()

        # Dataclass VO
        @dataclass
        class UserVo:
            username: str
            email: str
            age: int
            signup_time: datetime.datetime

        model = UserModel(
            user_name="bob",
            email="bob@example.com",
            signup_time="2023-01-01T12:00:00"
        )

        vo = BeanUtil.to_bean(model, UserVo)

        self.assertEqual(vo.username, "bob")  # 测试字段名转换
        self.assertEqual(vo.signup_time, datetime.datetime(2023, 3, 1, 14, 30))
        self.assertEqual(vo.age, 18)  # 测试默认值填充


    def test_vo_to_request_body(self) -> None:
        pass

