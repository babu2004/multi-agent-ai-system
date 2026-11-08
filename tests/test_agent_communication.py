
from agents.orchestrator import run_collaborative_workflow

query = "Find India's population and calculate 5% of it."

print(f"\n[USER] {query}")

answer = run_collaborative_workflow(query)

print("\n[FINAL ANSWER]")
print(answer)
