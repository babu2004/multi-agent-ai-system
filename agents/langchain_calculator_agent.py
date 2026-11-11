
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

from tools.calculator import calculate
from tools.time_tool import get_current_time

load_dotenv()


# 1. Create a LangChain tool
@tool
def calculator(a: float, b: float, operation: str) -> float:
    """Perform arithmetic using two numbers and an operation.

    Supported operations: +, -, *, /
    """
    return calculate(a, b, operation)
@tool
def current_time()-> str:
    """
    only returns the current time 
    """

    return get_current_time()


# 2. Connect to Groq
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=300,
)


# 3. Create the agent
agent = create_agent(
    model=model,
    tools=[calculator,current_time],
    system_prompt=(
        "You are a calculator assistant. "
        "Use the calculator tool for arithmetic. "
        "Base your answers on tool results."
    ),
)


# 4. Execute the agent
def run_langchain_calculator(query: str) -> str:

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return response["messages"][-1].content
