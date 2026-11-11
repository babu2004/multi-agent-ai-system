
from agents.langchain_calculator_agent import run_langchain_calculator

query = "get the current time and add its hours, minutes and seconds"

print(f"\n[USER] {query}")

answer = run_langchain_calculator(query)

print("\n[LANGCHAIN AGENT]")
print(answer)
