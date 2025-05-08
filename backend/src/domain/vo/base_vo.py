from dataclasses import dataclass
from typing import Any

@dataclass
class BaseVo:
    pass


@dataclass
class PaginationVo(BaseVo):
    total: int
    list: list[Any]
