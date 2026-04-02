from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import RunnableConfig


class State(TypedDict):
    input: str
    step1: str
    step2: str
    result: str


def step1(state: State, config: RunnableConfig):
    prefix = config.get("configurable", {}).get("prefix", "")
    text = f"{prefix}{state['input']}"
    state['step1'] = text
    print(f"[Step1] 使用 prefix = {prefix}")
    return state


def step2(state: State, config: RunnableConfig):
    suffix = config.get("configurable", {}).get("suffix", "")
    result = f"{state['step1']}{suffix}"
    print(f"[Step2] 使用 suffix = {suffix}")
    state["step2"] = result
    state["result"] = result
    return state


def build_graph():
    graph_build = StateGraph(State)
    graph_build.add_node("step1", step1)
    graph_build.add_node("step2", step2)
    graph_build.add_edge(START, "step1")
    graph_build.add_edge("step1", "step2")
    graph_build.add_edge("step2", END)

    graph = graph_build.compile()
    return graph


graph = build_graph()

config = RunnableConfig(
    configurable={
        "prefix": "[前缀]",
        "suffix": "[后缀]"
    }
)

result = graph.invoke({"input": "你好,LangGraph"}, config=config)

print("最终输出:", result)
