
from llm.provider import generate_with_tools
from agents.calculator_agent import run_calculator_agent
from agents.research_agent import run_research_agent

def choose_agent(query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Choose the best agent for the user's request. "
                "Return ONLY one word: calculator or general. "
                "Choose calculator for arithmetic or calculations. "
                "Choose general for all other requests."
            ),
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    response = generate_with_tools(
        messages=messages,
        tools=[],
    )

    choice = response.choices[0].message.content
    choice = (choice or "").strip().lower()

    if choice not in {"calculator", "general"}:
        raise ValueError(f"Invalid agent choice: {choice}")

    return choice


def run_orchestrator(query: str) -> str:
    agent_name = choose_agent(query)

    print(f"\n[ORCHESTRATOR] Selected agent: {agent_name}")

    if agent_name == "calculator":
        return run_calculator_agent(query)

    return (
        "No general-purpose specialist is implemented yet. "
        "Please try an arithmetic request."
    )

def run_collaborative_workflow(query: str) -> str:

    try:
        # Step 1: Research Agent 
        research_result = run_research_agent(query)

        # Step 2: Validate the result 
        if not isinstance(research_result, dict):
            raise ValueError("Invalid research result.")
        
        population = research_result.get("value")

        if not isinstance(population,(int,float)) or population <= 0:
            raise ValueError("Research Agent returned an invalid population.")

        print("\n[ORCHESTRATOR] Passing research result to Calculator Agent...")
        #step 3: Calculator Agent
        calculation_query = (f"Calulate {Population} multiplied by 0.05.")

        calculation_result = run_calculator_agent(calculation_query)

        if not calculation_result:
            raise ValueError("Calculator agent returned an empty result.")
    
        return (
        f"Based on our simulated population figure of "
        f"{Population:,} people, 5% is calculated as follows:\n"
        f"{calculation_result}"
        )

    except Exception as exc:
        print(f"\n [ORCHESTRATOR ERROR] {exc}")
        return f"Unable to complete the workflow: {exc}"
        
 