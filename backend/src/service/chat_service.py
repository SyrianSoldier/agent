from typing_extensions import override, Any
from src.service.base_service import BaseService
from src.service.log_service import LogService

class ChatService(BaseService):
    @override
    @classmethod
    @LogService.service_runtime_log(__name__, type_="start")
    async def start(cls) -> None:
        pass

    @override
    @classmethod
    @LogService.service_runtime_log(__name__, type_="end")
    async def end(cls) -> None:
        pass


    @classmethod
    def on_chat(self, message: str) -> str:
        return "111"


    @classmethod
    def save_chat_history(self, user_message:str, bot_message:str, extra: dict[str,Any]={}) -> None:
        pass

