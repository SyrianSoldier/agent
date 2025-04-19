from abc import ABC, abstractmethod
from typing import Never

from src.util.common_util import Singleton


class BaseService(ABC, Singleton):
    @classmethod
    @abstractmethod
    async def start(cls) -> Never:
        raise NotImplementedError()


    @classmethod
    @abstractmethod
    async def end(cls) -> Never:
        raise NotImplementedError()

