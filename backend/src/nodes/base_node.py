import functools

from abc import ABC, abstractmethod
from typing import Any, Callable
from typing_extensions import List

from src.domain.po.graph_po import NodeOutput, NodeInputItem
from src.domain.po.graph_po import State
from src.constants.input_value_alias import InputValueAlias


class BaseNode(ABC):
    """节点抽象基类"""

    def _parse_input(self,state:State, inputs: List[NodeInputItem]) -> List[NodeInputItem]:
        """
        处理输入占位符替换逻辑

        示例配置：
        ```json
        {
            "nodes": [
                {
                    "id": "start",
                    "type": "START",
                    "name": "开始节点",
                    "inputs": [
                        {
                            "name": "user_input",
                            "type": "string",
                            "value": "$USER_QUERY"  # ← 占位符将被实际输入替换
                        }
                    ]
                }
            ]
        }"
        """

        node_inputs: List[NodeInputItem] = []
        for input in inputs:
            node_input:NodeInputItem

            if isinstance(input.value, str):
                if input.value.startswith(InputValueAlias.STATE.value):
                    node_input = NodeInputItem(
                        name=input.name,
                        type=input.type,
                        value=state.get("result") #TODO:支持jsonpath语法
                    )
                elif input.value.startswith(InputValueAlias.USER_QUERY.value):
                    node_input = NodeInputItem(
                        name=input.name,
                        type=input.type,
                        value=state.get("query")
                    )

                node_inputs.append(node_input)

        return node_inputs

    @abstractmethod
    def execute(self, state: State, inputs: List[NodeInputItem], node_id:str) -> NodeOutput:
        """执行节点核心逻辑并生成输出结果。

        子类必须实现该方法来定义具体的节点行为。该方法接收运行时状态、输入数据及节点ID,
        处理后返回标准化的节点输出。

        Args:
            state (State): 运行时状态对象，用于在节点间传递上下文数据。应包含流程执行所需的共享状态信息。
            inputs (List[NodeInputItem]): 节点输入项列表，每个输入项包含：
                - name: 输入参数名称
                - type: 数据类型标识
                - value: 输入值（可能包含解析后的实际值或原始占位符）
            node_id (str): 当前节点的唯一标识符，格式为 `<节点类型>_<UUID>`,
                例如：`START_1a2b3c4d5e6f`

        Returns:
            NodeOutput: 标准化输出对象，包含：
                - node_type: 节点类型枚举
                - value: 处理后的输出值（任意类型）
                - node_id: 继承自输入参数的节点标识

        Example:
            class StartNode(BaseNode):
                def execute(self, state, inputs, node_id):
                    # 实现具体处理逻辑...
                    return NodeOutput(
                        node_type=NodeType.START,
                        value=processed_data,
                        node_id=node_id
                    )
        """
        pass



def input_adoptor(execute: Callable) -> Callable:

    @functools.wraps(execute)
    def wrapper(self: BaseNode, *args, **kwargs) -> Any:
        state: State = args[0]

        inputs: List[NodeInputItem] = args[1]
        assert isinstance(inputs, list)

        # 默认用基类的解析input方法，也可以由子类覆写_parse_input方法实现解析input
        new_inputs: List[NodeInputItem] = self._parse_input(state, inputs)
        return execute(self, state=state, inputs=new_inputs, node_id=args[2], **kwargs)

    return wrapper
