
from src.constants.node_type import NodeType

from src.nodes.base_node import BaseNode
from src.nodes.start_node import StartNode
from src.nodes.end_node import EndNode
from src.nodes.chat_node import ChatNode


class NodeFactory:
    NodeMap: dict[NodeType, BaseNode] = {
        NodeType.START: StartNode,
        NodeType.END: EndNode,
        NodeType.CHAT: ChatNode,
    }

    @classmethod
    def get_node_by_type(cls, node_type: NodeType) -> BaseNode:
        # pylint: disable=consider-iterating-dictionary
        if node_type not in cls.NodeMap.keys():
            raise ValueError(f"Unsupported node type: {node_type}")

        return cls.NodeMap.get(node_type)()
