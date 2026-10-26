
from agents.orchestrator import run_orchestrator


queries = [
    "What is 125 multiplied by 37, then divided by 5?",
    "Calculate 250 divided by 10.",
]

for query in queries:
    print(f"\n[USER] {query}")

    answer = run_orchestrator(query)

    print(f"[FINAL ANSWER] {answer}")
