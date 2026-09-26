from agents.agent import run_agent


query = "Calculate 125 multiplied by 37 and tell me the current time."

answer = run_agent(query)

print("\nFinal Answer:")
print(answer)