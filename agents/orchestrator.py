
from llm.provider import generate_with_tools
from agents.calculator_agent import run_calculator_agent


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
