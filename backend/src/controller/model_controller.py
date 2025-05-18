from .base_controller import BaseController
from src.service.chat_serssion_service import ChatSeesionService

class List(BaseController):
    async def get(self) -> None:
        self.return_success(data=vo)
