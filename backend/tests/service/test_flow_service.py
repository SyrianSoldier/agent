import json
from langgraph.graph.state import CompiledStateGraph
from src.service.flow_service import LangGraphBuilder
from src.types.graph_type import State
from src.constants.node_type import NodeType

class TestFlowService:
    @classmethod
    def setup_class(cls) -> None:
        pass

    @classmethod
    def teardown_class(cls) -> None:
        pass

    def test_langgraph_builder(self) -> None:
        with open("tests/resource/flow_template.json", "r", encoding="utf-8") as f:
            flow_template: str = f.read()

        builder: LangGraphBuilder = LangGraphBuilder()
        graph: CompiledStateGraph = builder.build_from_json(json.loads(flow_template))
        initial_state: State = {"query": "什么是大模型?", "result": {}}
        result_state: State = graph.invoke(initial_state)

        assert result_state is not None, "result_state不能为空"

        # TODO: 更友好的错误提示信息

        # 输出是否符合State格式
        for key in State.__annotations__.keys():
            assert result_state.get(key) is not None, f"result_state缺失{key}字段"

        # 动态校验每个节点的元数据

        seen_types = set()
        print(result_state.get("result"))
        for node_id, node_data in result_state.get("result").items():

            # 校验nodeId格式
            assert "_" in node_id, "node_id的格式应为 <NodeType>_<uuid>"

            # 校验NodeType
            node_type, uuid_part = node_id.split("_", 1)
            assert node_type in [member.name for member in NodeType], f"未找到NodeType:{node_type=}"
            assert len(uuid_part) >= 8, f"UUID部分至少8位:{uuid_part=}"

            # 校验字段存在性
            assert "nodeType" in node_data, "缺失nodeType字段"
            assert "nodeId" in node_data, "缺失nodeId字段"

            # 类型一致性校验
            # assert node_data["nodeType"] == node_type, f"nodeType与nodeId前缀不一致{node_data}"
            assert node_data["nodeId"] == node_id, "nodeId应自洽"

            seen_types.add(node_type)

        assert len(seen_types) >= 3, "至少应包含3个节点结果（START/任意节点/END）"
