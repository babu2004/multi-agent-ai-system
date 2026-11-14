
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool

from tools.calculator import calculate

load_dotenv()


# 1. Define the tool's input schema
class CalculatorInput(BaseModel):
    a: float = Field(description="First number")
    b: float = Field(description="Second number")
    operation: str = Field(
        description="Arithmetic operation: +, -, *, /"
    )


# 2. Create a CrewAI custom tool
class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = (
        "Perform arithmetic calculations using two numbers. "
        "Supports addition, subtraction, multiplication and division."
    )
    args_schema: type[BaseModel] = CalculatorInput

    def _run(
        self,
        a: float,
        b: float,
        operation: str
    ) -> float:
        return calculate(a, b, operation)


calculator_tool = CalculatorTool()


# 3. Configure the LLM
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("XAI_API_KEY"),
    temperature=0,
)


# 4. Create the agent
calculator_agent = Agent(
    role="Mathematical Calculator",
    goal="Solve calculations accurately using the calculator tool.",
    backstory=(
        "You are a mathematical specialist. "
        "Always use the calculator tool for arithmetic. "
        "Never invent calculation results."
    ),
    tools=[calculator_tool],
    llm=llm,
    verbose=True,
)


# 5. Define the task
calculation_task = Task(
    description=(
        "Calculate 125 multiplied by 37, "
        "then divide the result by 5. "
        "You MUST use the calculator tool for both operations."
    ),
    expected_output=(
        "The final numerical result with a brief explanation."
    ),
    agent=calculator_agent,
)


# 6. Create the crew
calculator_crew = Crew(
    agents=[calculator_agent],
    tasks=[calculation_task],
    process=Process.sequential,
    verbose=True,
)


def run_crewai_calculator():
    return calculator_crew.kickoff()


if __name__ == "__main__":
    print("\n[CREWAI RESULT]")
    print(run_crewai_calculator())
