
from agents.state import AgentState

state = AgentState(
    plan=[
        {
            "id": 1,
            "description": "Multiply 125 by 37",
            "status": "pending",
        },
        {
            "id": 2,
            "description": "Divide the result by 5",
            "status": "pending",
        },
    ]
)

state.complete_task(1, "4625")
state.complete_task(2, "925.0")

print("\n[AGENT STATE]")
print("Plan:", state.plan)
print("Results:", state.task_results)
