from abc import ABC, abstractmethod

from src.util.common_util import Singleton


class BaseService(ABC, Singleton):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def end(self) -> None:
        pass
