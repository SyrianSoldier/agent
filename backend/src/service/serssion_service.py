from typing_extensions import override
from .base_service import BaseService
from src.models.database.session_model import SessionModel

class SeesionService(BaseService):
    @override
    @classmethod
    def start(cls) -> None:
        pass

    @override
    @classmethod
    def end(cls) -> None:
        pass
