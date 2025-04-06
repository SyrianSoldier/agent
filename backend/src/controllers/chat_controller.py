from typing import Any
import tornado.websocket
import tornado.httputil
from typing_extensions import  Union, override
from src.service.chat_service import ChatService
from util.env_util import EnvUtil

class ChatController(tornado.websocket.WebSocketHandler):
    def __init__(
        self,
        application: tornado.web.Application,
        request: tornado.httputil.HTTPServerRequest,
        **kwargs: Any
    ) -> None:
        super().__init__(application, request, **kwargs)

    @override
    def open(self, *args: Any, **kwargs: Any) -> None:
        print("WebSocket 连接已建立")

    @override
    def on_close(self) -> None:
        print("WebSocket 连接已关闭")

    @override
    def data_received(self, chunk: Any) -> None:
        pass

    @override
    def on_message(self, message: Union[str, bytes]) -> None:
        if isinstance(message, str):
            bot_message:str = ChatService().on_chat(message)
            ChatService().save_chat_history(user_message=message, bot_message=bot_message)

            return
            # TODO
        else:
            pass
        print(message)

    @override
    def check_origin(self, origin: str) -> bool:
        return origin in EnvUtil.get_cur_env_config().get("allowed_origins")
