from typing import override

from src.constants.node_type import NodeType
from src.domain.po.graph_po import NodeOutput, NodeInputItem
from src.domain.po.graph_po import State


from .base_node import BaseNode, input_adoptor

class EndNode(BaseNode):
    node_type: str = NodeType.END

    @override
    @input_adoptor
    def execute(self, state: State, inputs: list[NodeInputItem],node_id:str) -> NodeOutput:
        return NodeOutput(node_type=NodeType.START,value=111,node_id=node_id)
