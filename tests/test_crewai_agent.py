from agents.crewai_calculator import run_crewai_calculator

print("\n[USER] Calculate 125 * 37, then divide by 5.")
result = run_crewai_calculator()

print("\n[FINAL ANSWER]")

print(result)
