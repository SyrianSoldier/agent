from abc import ABC, abstractmethod

from src.util.common_util import Singleton


class BaseService(ABC, Singleton):
    @abstractmethod
    @classmethod
    def start(cls) -> None:
        pass

    @abstractmethod
    @classmethod
    def end(cls) -> None:
        pass
