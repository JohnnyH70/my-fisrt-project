from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import RunnableConfig
from typing import TypedDict


class State(TypedDict):
    total: int  # 当前累加总和
    new_value: int  # 新输入的数字


# 定义节点: 执行累加逻辑
def add_node(state: State, config: RunnableConfig):
    old_total = state.get("total", 0)
    print(f"old_total--->{old_total}")

    new_value = state["new_value"]

    new_total = old_total + new_value
    state["total"] = new_total
    return state


# 构件图
def build_graph():
    graph_build = StateGraph(State)
    graph_build.add_node("add", add_node)
    graph_build.add_edge(START, "add")
    graph_build.add_edge("add", END)

    memory = InMemorySaver()
    graph = graph_build.compile(memory)
    return graph


if __name__ == '__main__':
    graph = build_graph()
    # === 第一次调用 ===
    config1 = RunnableConfig(configurable={
        "thread_id": "12345"
    })
    result1 = graph.invoke({"new_value": 5}, config=config1)
    print(f"结果1:{result1}")

    # === 第二次调用 同一个线程 累加===
    result2 = graph.invoke({"new_value": 7}, config=config1)
    print(f"结果2:{result2}")

    # === 第三次调用 不同线程 全新开始===
    config2 = RunnableConfig(configurable={
        "thread_id": "67890"
    })

    result3 = graph.invoke({"new_value": 10}, config=config2)
    print(f"结果3:{result3}")
