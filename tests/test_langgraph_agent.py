
from agents.langgraph_calculator_agent import run_langgraph_calculator

query = "Calculate 125 multiplied by 37, then divide the result by 5."

print(f"\n[USER] {query}")

answer = run_langgraph_calculator(query)

print("\n[LANGGRAPH AGENT]")
print(answer)
