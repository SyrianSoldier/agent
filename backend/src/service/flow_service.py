from typing import Any
from typing_extensions import override

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.constants.node_type import NodeType
from src.nodes.base_node import BaseNode
from src.nodes.node_factory import NodeFactory
from src.domain.po.graph_po import Graph, Node, Edge, NodeInputItem, NodeOutput
from src.service.base_service import BaseService
from src.domain.po.graph_po import State
from src.service.log_service import LogService

class FlowService(BaseService):
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


class LangGraphBuilder:
    """通过json构建Langgraph"""
    def __init__(self) -> None:
        self.langgraph:StateGraph = StateGraph(State)


    def node_reducer_factory(self, node_type:NodeType, node_id:str, node_inputs:list[NodeInputItem]) -> State:
        def reducer(state:State): # type: ignore
            """图状态的reducer函数,请保持此函数是纯函数"""
            node_ins:BaseNode = NodeFactory.get_node_by_type(node_type)
            node_output:NodeOutput = node_ins.execute(state, node_inputs, node_id)
            state:State = {
                **state,
                "result": {
                    **state.get("result"),
                    node_id: node_output.to_dict()
                }
            }
            return state
        return reducer


    def _build_nodes(self, nodes: list[Node]) -> None:
        for node in nodes:
            if node.type is NodeType.START:
                self.langgraph.set_entry_point(node.id)
            elif node.type is NodeType.END:
                self.langgraph.set_finish_point(node.id)

            self.langgraph.add_node(node.id, self.node_reducer_factory(node.type,node.id,node.inputs))


    def _build_edges(self,edges: list[Edge]) -> None:
        for edge in edges:
            self.langgraph.add_edge(edge._from, edge.to)


    def build_from_json(self, graph_json_dict: dict[str, Any]) -> CompiledStateGraph:
        try:
            user_graph:Graph = Graph.from_dict(graph_json_dict)
        except ValueError as e:
            raise ValueError(
                "Invalid JSON format detected. Please ensure the graph data matches the required schema."
            ) from e

        self._build_nodes(user_graph.nodes)
        self._build_edges(user_graph.edges)

        return self.langgraph.compile()
