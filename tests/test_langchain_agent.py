
from agents.langchain_calculator_agent import run_langchain_calculator

query = "Calculate 125 multiplied by 37, then divide the result by 5."

print(f"\n[USER] {query}")

answer = run_langchain_calculator(query)

print("\n[LANGCHAIN AGENT]")
print(answer)
