from typing import override

from src.constants.node_type import NodeType
from src.domain.po.graph_po import NodeOutput, NodeInputItem
from src.domain.po.graph_po import State


from .base_node import BaseNode,input_adoptor

class ChatNode(BaseNode):
    node_type: str = NodeType.CHAT

    @override
    @input_adoptor
    def execute(self, state: State, inputs: list[NodeInputItem],node_id:str) -> NodeOutput:
        #TODO 支持可以选择多个模型
        mock_answer:str = "你好我是chatGPT,你问的问题我不知道"
        return NodeOutput(node_type=NodeType.START,value=mock_answer,node_id=node_id)
