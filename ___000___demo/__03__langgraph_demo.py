# 加入记忆 存放在硬盘中
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver


class SqliteManager:
    def __init__(self):
        print("初始化 SqliteManager")
        self.memory_ctx = SqliteSaver.from_conn_string("checkpoint.db")
        self.memory = self.memory_ctx.__enter__()

    def close(self):
        print("关闭 SqliteManager")
        self.memory_ctx.__exit__(None, None, None)


class State(TypedDict, total=False):
    total: int
    new_value: int


def add_node(state: State):
    old_total = state.get("total", 0)
    print(f"旧 total:{old_total}")

    new_value = state.get("new_value", 0)
    print(f"本次 new_value:{new_value}")

    new_total = old_total + new_value
    return {
        "total": new_total,
        "new_value": new_value
    }


def build_graph(memory):
    graph_builder = StateGraph(State)
    graph_builder.add_node("add_node", add_node)
    graph_builder.add_edge(START, "add_node")
    graph_builder.add_edge("add_node", END)

    return graph_builder.compile(checkpointer=memory)


splite_manager = SqliteManager()
graph = build_graph(splite_manager.memory)

if __name__ == '__main__':
    # try:
    #     # ========================
    #     # 同一个 thread_id: "aaabbb" 调用 2 次 → 记忆累加
    #     # ========================
    #     config1 = RunnableConfig(configurable={"thread_id": "aaabbb"})
    #
    #     # 第一次：total = 0 + 100 = 100
    #     result1 = graph.invoke({"new_value": 100}, config=config1)
    #     print(f"【aaabbb】第一次结果: {result1}")
    #
    #     # 第二次：total = 100 + 20 = 120  ✅ 这里会加载记忆！
    #     result2 = graph.invoke({"new_value": 20}, config=config1)
    #     print(f"【aaabbb】第二次结果: {result2}")
    #
    #     print("=" * 50)
    #
    #     # 另一个 thread_id，独立记忆
    #     config2 = RunnableConfig(configurable={"thread_id": "cccddd"})
    #     result3 = graph.invoke({"new_value": 20}, config=config2)
    #     print(f"【cccddd】第一次结果: {result3}")
    #
    # finally:
    #     splite_manager.close()

    try:
        config1 = RunnableConfig(configurable={"thread_id": "aaabbb"})
        # 只调用第二次
        result2 = graph.invoke({"new_value": 20}, config=config1)
        print(f"【重启后】结果: {result2}")
    finally:
        splite_manager.close()
