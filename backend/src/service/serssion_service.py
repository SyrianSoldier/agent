from typing_extensions import override
from .base_service import BaseService
from src.models.database.session_model import SessionModel

class SeesionService(BaseService):
    @override
    def start(self) -> None:
        pass

    @override
    def end(self) -> None:
        pass
