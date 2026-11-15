
from agents.crewai_multi_agent import run_multi_agent_crew


def test_crewai_multi_agent():
    print("\n[USER] Calculate 5% of India's population.")

    result = run_multi_agent_crew()

    print("\n[FINAL ANSWER]")
    print(result)


if __name__ == "__main__":
    test_crewai_multi_agent()
