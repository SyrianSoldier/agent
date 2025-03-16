from typing_extensions import TypedDict, Any

class State(TypedDict):
    """
    流程状态容器


    result:{
        <NodeType>_<uuid>: {
            node_type: 节点的NodeType,
            value: 真正的节点输出数据,
            node_id: <NodeType>_<uuid>
        }

        ...
    }
    """

    # 记录每个节点的执行结果. 格式: {节点id: 该节点的输出}
    result: dict[str, Any]
    # 记录用户的输入
    query: str
