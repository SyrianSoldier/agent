from typing_extensions import override,List

from src.constants.node_type import NodeType
from src.models.domain.graph import NodeOutput, NodeInputItem
from src.types.graph_type import State

from .base_node import BaseNode,input_adoptor

class StartNode(BaseNode):
    node_type: str = NodeType.START

    @override
    @input_adoptor
    def execute(self, state: State, inputs: List[NodeInputItem],node_id:str) -> NodeOutput:
        print(inputs)
        return NodeOutput(node_type=NodeType.START,value=111,node_id=node_id)
