from abc import ABC, abstractmethod

from src.util.common_util import Singleton


class BaseService(ABC, Singleton):
    @classmethod
    @abstractmethod
    def start(cls) -> None:
        raise NotImplementedError()


    @classmethod
    @abstractmethod
    def end(cls) -> None:
        raise NotImplementedError()
