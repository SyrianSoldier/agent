import asyncio

from .base_llm import BaseLLM, BaseRequestParams, ModelType, ModelPlatform
from dataclasses import dataclass, field, asdict
import dashscope
from langchain_core.outputs import GenerationChunk
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Iterator, override, cast

@dataclass
class RequestParams(BaseRequestParams):
    """所有的request params不应该包含messages, 这个要由前端表单去填
    """
    api_key:str|None = None
    stream:bool = True
    base_url:str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model:str = "qwq-plus-latest"

#TODO: 重构, 看下如何更好的langchain结合,现在先能调用通就行
#TODO: 重构, 继承runtime日志,看下怎么个添加法
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
            raise ValueError("调用模型前需要先设置请求参数")

        self.request_params.stream = False


        response = dashscope.Generation.call(**{
            **asdict(self.request_params),
            "messages": [
                {"role": "user", "content": prompt},
                {'role': 'system', 'content': 'You are a helpful assistant.'}
            ]
        })
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
            raise ValueError("调用模型前需要先设置请求参数")

        responses = dashscope.Generation.call(**{
            **asdict(self.request_params),
            "messages": [
                {"role": "user", "content": prompt},
                {'role': 'system', 'content': 'You are a helpful assistant.'}
            ]
        })

        for response in responses:
            output_char = response.output.choices[0].message.content
            yield GenerationChunk(text=output_char)


if __name__ == "__main__":
    async def run_qwen_plus() -> None:
        llm = QwenPlus()
        llm.request_params = RequestParams(
            api_key="your api key",
        )
        async for token in llm.astream("你是个聪明的助手"):
            print(token, end="", flush=True)

    asyncio.run(run_qwen_plus())




