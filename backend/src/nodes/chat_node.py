from typing_extensions import override,List

from src.constants.node_type import NodeType
from src.models.domain.graph import NodeOutput, NodeInputItem
from src.types.graph_type import State

from .base_node import BaseNode,input_adoptor

class ChatNode(BaseNode):
    node_type: str = NodeType.CHAT

    @override
    @input_adoptor
    def execute(self, state: State, inputs: List[NodeInputItem],node_id:str) -> NodeOutput:
        #TODO 支持可以选择多个模型
        mock_answer:str = "你好我是chatGPT,你问的问题我不知道"
        return NodeOutput(node_type=NodeType.START,value=mock_answer,node_id=node_id)
