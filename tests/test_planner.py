from agents.planner import create_plan

query = (
    "Calculate 125 multiplied by 37, "
    "divide the result by 5, "
    "and tell me whether the answer is greater than 900."
)

plan = create_plan(query)

print("\n[ PLAN ]")

for task in plan:
    print(
        f"{task['id']}. "
        f"{task['description']} "
        f"[{task['status']}]"
    )