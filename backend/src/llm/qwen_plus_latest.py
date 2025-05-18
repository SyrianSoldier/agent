import asyncio

from .base_llm import BaseLLM, BaseRequestParams, ModelType, ModelPlatform
from dataclasses import dataclass, field, asdict
import dashscope
from langchain_core.outputs import GenerationChunk
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Iterator, Never, override, cast


@dataclass
class RequestParams(BaseRequestParams):
    api_key:str|None = None
    messages:list[dict[str,Any]] = field(default_factory=list)
    stream:bool = True
    base_url:str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model:str = "qwq-plus-latest"

#TODO: 重构,看下如何更好的langchain结合,现在先能调用通就行
class QwenPlus(BaseLLM[RequestParams]):
    request_params:RequestParams|None = None
    model_name:str = "qwq-plus-latest"
    model_type:ModelType = ModelType.Cloud
    model_platform:ModelPlatform = ModelPlatform.Dashscope
    model_doc:str = r"https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?spm=a2c4g.11186623.0.i1"

    @override
    def _call(
        self,
        prompt: str,
        stop: list[str]|None = None,
        run_manager: CallbackManagerForLLMRun|None = None,
        **kwargs: Any,
    ) -> str:
        if self.request_params is None:
            #TODO: 完善错误信息
            raise ValueError()

        self.request_params.stream = False

        self.request_params.messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ]

        response = dashscope.Generation.call(**asdict(self.request_params))
        return cast(str, response.output.choices[0].message.content)


    @override
    def _stream(
        self,
        prompt: str,
        stop: list[str]|None = None,
        run_manager: CallbackManagerForLLMRun|None = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        if self.request_params is None:
            #TODO: 完善错误信息
            raise ValueError()

        self.request_params.messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ]

        responses = dashscope.Generation.call(**asdict(self.request_params))

        for response in responses:
            output_char = response.output.choices[0].message.content
            yield GenerationChunk(text=output_char)


if __name__ == "__main__":
    async def run_qwen_plus() -> None:
        llm = QwenPlus()
        llm.request_params = RequestParams(
            api_key="sk-d349b80d80bf4e77a2de968c868947bc",
        )
        async for token in llm.astream("你是个聪明的助手"):
            print(token, end="", flush=True)

    asyncio.run(run_qwen_plus())





