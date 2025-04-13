from typing_extensions import override, Union, Any, Dict
from src.service.base_service import BaseService


class ChatService(BaseService):
    @override
    @classmethod
    def start(cls) -> None:
        pass

    @override
    @classmethod
    def end(cls) -> None:
        pass

    def on_chat(self, message: str) -> str:
        return "111"

    def save_chat_history(self, user_message:str, bot_message:str, extra: Dict[str,Any]={}) -> None:
        pass

