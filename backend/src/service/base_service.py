from abc import ABC, abstractmethod
from typing import Never


class BaseService(ABC):
    @classmethod
    @abstractmethod
    async def start(cls) -> Never:
        raise NotImplementedError()


    @classmethod
    @abstractmethod
    async def end(cls) -> Never:
        raise NotImplementedError()

