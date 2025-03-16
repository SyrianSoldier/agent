import uuid
from typing import Any, Dict, List, Optional

from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard

from src.constants.node_type import NodeType

@dataclass
class Position(JSONWizard):
    """节点在画布上的位置"""

    x: float
    y: float


@dataclass
class NodeInputItem(JSONWizard):
    """节点一个输入的定义"""

    # 输入名称（对应函数参数名）
    name: str
    type: str
    value: Any


@dataclass
class NodeOutput(JSONWizard):
    """节点输出定义"""

     #TODO: 这个类继承JSONWizard，会自动实现to_dict方法，但是会把snake的key转成camal，如 node_id --> NodeId, 有时间研究下JSONWizard的转换

    # 节点类型
    node_type: NodeType
    # 输出的内容
    value: Any
    # 节点id
    node_id:str = field(default=None)

    def __post_init__(self):
        """后初始化处理,生成默认node_id"""
        if self.node_id is None:
            self.node_id = f"{str(self.node_type)}_{uuid.uuid4().hex}"


@dataclass
class NodeConfig(JSONWizard):
    """节点配置参数(分为自定义配置和通用配置)"""

    # 超时时间（秒）
    timeout: int = 30
    # 最大重试次数
    max_retries: int = 3
    # 每个节点的自定义参数（JSON格式）
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Node(JSONWizard):
    """节点定义"""

    # 节点唯一标识
    id: str
    # 节点类型（task/condition/start/end等）
    type: NodeType
    # 显示名称
    name: str
    # 节点位置信息
    position: Position
    # 输入配置
    inputs: List[NodeInputItem] = field(default_factory=list)
    # 节点配置参数
    config: NodeConfig = field(default_factory=NodeConfig)
    # 节点描述
    description: Optional[str] = None

    # @classmethod
    # def _pre_from_dict(cls, o: JSONObject) -> JSONObject:
    #     """预处理dict, 文档:https://dataclass-wizard.readthedocs.io/en/latest/advanced_usage/serializer_hooks.html"""
    #     for member in NodeType:
    #         if str(member) == o["type"]:
    #             o["type"] = member
    #     return o


@dataclass
class Edge(JSONWizard):
    """边的定义"""

    _from: str
    to: str


@dataclass
class GraphMetadata(JSONWizard):
    """图的元数据"""

    name: str = "langgraph builder json"
    version: str = "1.0.0"
    description: Optional[str] = None


@dataclass
class Graph(JSONWizard):
    """
    完整的图定义, 对应json格式可参考tests/resource/flow_template.json
    """

    nodes: List[Node]
    edges: List[Edge]
    metadata: GraphMetadata = field(default_factory=GraphMetadata)
