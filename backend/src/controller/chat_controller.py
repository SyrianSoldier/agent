import json
from typing import Any
from dataclasses import dataclass, field
import tornado.websocket
import tornado.httputil
from typing_extensions import override
from src.service.log_service import LogService
from src.domain.model.message_history_model import MessageHistoryModel
from src.service.message_history_service import MessageHistoryService
from src.util.bean_util import BeanUtil
from src.util.json_util import JsonUtil
from src.service.chat_service import ChatService

@dataclass
class ChatRequestDto():
    model_name:str|None = None
    messages: str|None = None
    request_params:dict[str, Any] = field(default_factory=dict)  # 对应的模型的请求参数


class ChatController(tornado.websocket.WebSocketHandler):
    def __init__(
        self,
        application: tornado.web.Application,
        request: tornado.httputil.HTTPServerRequest,
        **kwargs: Any
    ) -> None:
        super().__init__(application, request, **kwargs)

        self.session_uuid:str|None = None

    @override
    def check_origin(self, origin: str) -> bool:
        return True


    @override
    async def open(self, *args: Any, **kwargs: Any) -> None:
        session_uuid:str|None = self.get_query_argument("session_uuid",default=None)

        assert session_uuid is not None, "session_uuid不能为空"

        history_msgs: list[MessageHistoryModel] = await MessageHistoryService.get_chat_history_list(session_uuid)
        history_msg_json = [BeanUtil.to_bean(history_message, dict, convert=True) for history_message in history_msgs]
        self.write_message(JsonUtil.dumps(history_msg_json))
        LogService.runtime_logger.info("WebSocket 连接已建立")


    @override
    def on_close(self) -> None:
        LogService.runtime_logger.info("WebSocket 连接已关闭")


    @override
    async def on_message(self, message: str) -> None: # type:ignore
        # 获取参数
        session_uuid:str|None = self.get_query_argument("session_uuid",default=None)
        request_dict:dict[str, Any] = JsonUtil.loads(message)
        chat_request_dto = BeanUtil.to_bean(request_dict, ChatRequestDto)

        assert session_uuid is not None, "session_uuid不能为空"
        assert chat_request_dto.model_name is not None, "模型名称不能为None"
        assert chat_request_dto.request_params is not None, "模型请求参数不能为None"
        assert chat_request_dto.messages is not None, "模型消息参数不能为None"

        await ChatService.on_chat_stream(
            prompt=chat_request_dto.messages,
            model_name=chat_request_dto.model_name,
            request_params=chat_request_dto.request_params,
            session_uuid=session_uuid,
            write_message= lambda message: self.write_message(message)
        )
