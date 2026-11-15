import os 

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

from agents.crewai_calculator import calculator_tool

load_dotenv()

# Configure the llm 

llm = LLM(
    model = "groq/openai/gpt-oss-120b",
    api_key = os.getenv("XAI_API_KEY"),
    temperature = 0,
)

# Create the research Agent

research_agent = Agent(
    role = "Research Specialist",
    goal = "Extract accurate information from the procided dataset.",
    backstory = (
        "you are a research specialist."
        "you carefully extract facts and return clear,"
        "sturctured information. Never invent Data."
    ),
    llm= llm,
    verbose = True,
)

# Create the calculator Agent

calculator_agent = Agent(
    role = "Mathematical Analyst",
    goal = "Perform accurate Calculation using the calculator tool.",
    backstory = (
        "you are a mathematical specialist."
        "you use the calculator tool for every calculation "
        "and base your ansers on its results."
    ),
    tools = [calculator_tool],
    llm = llm,
    verbose=True,
)

# Define the research task
research_task = Task(
    description = (
        "Use ONLY this simulated DATASET:\n"
        "country: India\n"
        "Population: 1,400,000,000 people \n\n"
        "Extract the country and population."
        "Return the population as a clear numerical value."

    ),

    expected_output = (
        "The Country name and its population as a number."
    ),
    agent = research_agent,
)

# Define the calculation Task
calculation_task = Task(
    description = (
        "Read the research result from your task context."
        "Calculate 5 percent of the reported population."
        "You Must use the calculator tool."
        "Explain the calculation and provide the final answer."
    ),
    expected_output = (
        "the calculation steps and final restult in people."
    ),
    agent = calculator_agent,
    context = [research_task],
)

# create the Crew

crew = Crew(
    agents = [research_agent,calculator_agent],
    tasks = [research_task, calculation_task],
    process = Process.sequential,
    verbose = True,
)

# run the workflow
def run_multi_agent_crew():
    return crew.kickoff()

if __name__=="__main__":
    result = run_multi_agent_crew()

    print("\n[FINAL MULTI-AGENT RESULT]")
    print(result)