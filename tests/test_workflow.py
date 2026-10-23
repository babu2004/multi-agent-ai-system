
from agents.workflow import run_planned_workflow


query = (
    "Calculate 125 multiplied by 37, "
    "divide the result by 5, "
    "and determine whether the final result is greater than 900."
)

state = run_planned_workflow(query)

print("\n[FINAL STATE]")
print("Steps:", state.steps)
print("Errors:", state.errors)
print("Results:", state.task_results)

for task in state.plan:
    print(f"Task {task['id']}: {task['status']}")
