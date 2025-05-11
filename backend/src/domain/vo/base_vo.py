from dataclasses import dataclass
from typing import Any
from src.util.validate_util import ValidateUtil
from src.util.bean_util import BeanUtil

@dataclass
class BaseVo:
    pass


@dataclass
class PaginationVo(BaseVo):
    total: int
    list: list[Any]

    def __post_init__(self) -> None:
        # 对list进行dict处理
        if not self.list:
            return

        convert_list:list[Any] = []
        for item in self.list:
            if ValidateUtil.is_user_defined_class_ins(item):
                convert_list.append(
                    BeanUtil.to_bean(item, dict)
                )

        self.list = convert_list
