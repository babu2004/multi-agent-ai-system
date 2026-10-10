from agents.agent import run_agent


query = "Calculate 125 multiplied by 37, divide the result by 5, and tell me whether the answer is greater than 900."

answer = run_agent(query)

print("\nFinal Answer:")
print(answer)