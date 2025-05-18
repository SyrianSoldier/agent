import json
from typing import Any, override
from langchain_core.language_models.llms import LLM
from enum import Enum
from dataclasses import dataclass
from abc import  ABC

class ModelType(Enum):
    Cloud = "云端模型"
    Local = "本地模型"


class ModelPlatform(Enum):
    Dashscope = "阿里百炼"


@dataclass
class BaseRequestParams():
    pass


class BaseLLM[T: BaseRequestParams](LLM):
    """tip: langchain的LLM继承自pydantic, 所以实例属性看起来像类属性
    """
    request_params:T|None = None # 运行时修改该属性, 动态发
    model_name:str
    model_type:ModelType
    model_doc:str
    model_platform:ModelPlatform


    @property
    @override
    def _identifying_params(self) -> dict[str, Any]:
        """用于帮助识别模型和打印 LLM; 应该返回一个字典。这是一个 @property。
        """
        return {
            "model_name": getattr(self.request_params, "model_name", None) or self.__class__.__name__,
            "model_type": self.model_type.value,
            "model_platform": self.model_platform.value,
            "model_doc": self.model_doc,
        }

    @property
    @override
    def _llm_type(self) -> str:
        """返回字符串的属性，仅用于日志记录目的。"""
        return json.dumps(self._identifying_params)
