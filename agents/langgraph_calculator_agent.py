
from typing import Annotated

from typing_extensions import TypedDict

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.messages import SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


from tools.calculator import calculate

load_dotenv()
# 1. Define our calculator tool

@tool
def calculator(a: float, b: float, operation: str) -> float:
    """Perform arithmetic using two numbers.

    Supported operations: add, subtract, multiply, divide.
    """

    operation_mapping = {
        "add": "+",
        "addition": "+",
        "subtract": "-",
        "subtraction": "-",
        "multiply": "*",
        "multiplication": "*",
        "divide": "/",
        "division": "/",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
    }

    normalized_operation = operation.lower().strip()

    if normalized_operation not in operation_mapping:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return calculate(
        a,
        b,
        operation_mapping[normalized_operation]
    )



tools = [calculator]


# 2. Connect our Groq model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=300,
)

model_with_tools = model.bind_tools(tools)


# 3. Define shared graph state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 4. Define the LLM node
def llm_call(state: AgentState):
    response = model_with_tools.invoke(
        [
            SystemMessage(
                content=(
                    "You are a calculator assistant. "
                    "Use the calculator tool for arithmetic. "
                    "Base your answers on tool results."
                )
            )
        ] + state["messages"]
    )

    return {"messages": [response]}


# 5. Create the tool node
tool_node = ToolNode(tools=tools)


# 6. Build the graph
builder = StateGraph(AgentState)

builder.add_node("llm", llm_call)
builder.add_node("tools", tool_node)

builder.add_edge(START, "llm")

builder.add_conditional_edges(
    "llm",
    tools_condition,
)

builder.add_edge("tools", "llm")


# 7. Compile the graph
agent = builder.compile()


# 8. Run the agent
def run_langgraph_calculator(query: str) -> str:
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return response["messages"][-1].content
