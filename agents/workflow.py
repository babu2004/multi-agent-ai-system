
from agents.planner import create_plan
from agents.state import AgentState
from agents.task_executor import execute_task


def run_planned_workflow(query: str) -> AgentState:
    state = AgentState(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ]
    )

    state.plan = create_plan(query)

    print("\n[PLAN]")
    for task in state.plan:
        print(f"{task['id']}. {task['description']} [pending]")

    for task in state.plan:
        task_id = task["id"]
        description = task["description"]

        # Skip tasks if an earlier task failed or was skipped.
        dependencies = [
            previous
            for previous in state.plan
            if previous["id"] < task_id
        ]

        if any(
            previous["status"] != "completed"
            for previous in dependencies
        ):
            task["status"] = "skipped"
            print(
                f"[TASK SKIPPED] {task_id}: "
                "an earlier task did not complete"
            )
            continue

        state.steps += 1

        try:
            result = execute_task(
                description,
                state.task_results,
            )

            state.complete_task(task_id, result)
            print(f"[TASK COMPLETED] {task_id}: {result}")

        except Exception as exc:
            state.fail_task(task_id, str(exc))
            state.errors += 1
            print(f"[TASK FAILED] {task_id}: {exc}")

    # IMPORTANT: return only after processing the plan.
    return state
