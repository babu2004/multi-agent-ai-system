
import os

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

from agents.crewai_calculator import calculator_tool

load_dotenv()


# 1. Configure the LLM
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("XAI_API_KEY"),
    temperature=0,
)


# 2. Create specialist agents
research_agent = Agent(
    role="Research Specialist",
    goal="Extract accurate information from the provided dataset.",
    backstory=(
        "You are a careful research specialist. "
        "You only use the supplied dataset and never invent facts."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


calculator_agent = Agent(
    role="Mathematical Analyst",
    goal="Perform accurate calculations using the calculator tool.",
    backstory=(
        "You are a mathematical specialist. "
        "Always use the calculator tool for arithmetic."
    ),
    tools=[calculator_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


# 3. Define tasks
research_task = Task(
    description=(
        "Extract India's population from this simulated dataset:\n"
        "Country: India\n"
        "Population: 1,400,000,000 people\n\n"
        "Return the country and population clearly."
    ),
    expected_output="Country name and numerical population.",
    agent=research_agent,
)


calculation_task = Task(
    description=(
        "Calculate 5% of India's population using the "
        "research result. You MUST use the calculator tool. "
        "Explain the calculation."
    ),
    expected_output=(
        "The calculation steps and final answer in people."
    ),
    agent=calculator_agent,
)


# 4. Create the hierarchical crew
crew = Crew(
    agents=[research_agent, calculator_agent],
    tasks=[research_task, calculation_task],
    process=Process.hierarchical,
    manager_llm=llm,
    verbose=True,
)


# 5. Execute
def run_hierarchical_crew():
    return crew.kickoff()


if __name__ == "__main__":
    result = run_hierarchical_crew()

    print("\n[HIERARCHICAL CREW RESULT]")
    print(result)
