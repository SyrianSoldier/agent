from typing import Callable, Literal, TypedDict
from typing_extensions import override, Any
from src.service.base_service import BaseService
from src.service.log_service import LogService
from src.llm.base_llm import BaseLLM, BaseRequestParams
from src.llm.qwen_plus_latest import QwenPlus, RequestParams as QwenPlusRequestParams
from src.util.bean_util import BeanUtil
from src.service.message_history_service import MessageHistoryService
from src.domain.model.message_history_model import MessageHistoryModel, ChatRole

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

    # 所有的聊天模型要从这里注册,才能使用
    all_model:list[dict[Literal["request_params","instance"], Any]] = [
        {
            "instance": QwenPlus(),
            "request_params": QwenPlusRequestParams
        }
    ]

    @classmethod
    async def get_model_list(cls) -> list[dict[str, Any]]:
        return [
            {
                "model_name": model_info["instance"].model_name,
                "request_params": BeanUtil.to_bean(model_info["request_params"], dict),
            }
            for model_info in cls.all_model
        ]


    @classmethod
    async def on_chat_stream(
        cls,
        prompt: str,    # 问模型啥问题
        model_name:str, # 调用的模型名称
        request_params: dict[str, Any], # 模型的请求参数
        session_uuid:str, # 本次聊天归属的聊天会话
        write_message:Callable[[Any], Any] # 一个函数,需要实现将模型生成的消息写到哪里去
    ) -> None:
        # 校验模型是否可用
        model_info = list(filter(lambda model_info: model_info["instance"].model_name == model_name, cls.all_model))[0]
        assert model_info is not None, f"不支持该模型:{model_name}"

        # 取出模型, 构建请求参数
        llm:BaseLLM[Any] = model_info["instance"] #type:ignore
        RequestParams: BaseRequestParams = model_info["request_params"]
        llm.request_params = BeanUtil.to_bean(request_params, RequestParams)

        # 使用大模型发送请求
        bot_message:str = ""
        thinking_content:str|None = None # TODO:处理思考内容

        async for token in llm.astream(prompt):
            if token.strip() != "":
                write_message(token)
                bot_message += token

        # 创建历史消息
        message_history = MessageHistoryModel(
            content=bot_message,
            role=ChatRole.ASSISTANT,
            session_uuid=session_uuid,
            thinking_content=thinking_content
        )

        await MessageHistoryService.create_chat_history(message_history)



