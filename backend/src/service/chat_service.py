from typing_extensions import override, Union, Any, Dict
from src.service.base_service import BaseService


class ChatService(BaseService):
    @override
    def start(self) -> None:
        pass

    @override
    def end(self) -> None:
        pass

    def on_chat(self, message: str) -> str:
        return "111"

    def save_chat_history(self, user_message:str, bot_message:str, extra: Dict[str,Any]={}) -> None:
        pass

