import json
from llm.provider import generate_with_tools

def create_plan(query:str) -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": """
You are a task planner for an AI agent.

Break the user's request into a sequence of small,
ordered, actionable tasks.

Return ONLY valid JSON in this format:
{
    "tasks": [
        {
            "id": 1,
            "description": "Describe the task",
            "status": "pending"
        }
    ]
}

Rules:
- Tasks must be ordered logically.
- Each task must have a clear objective.
- Keep tasks concise.
- Do not execute tasks or invent results.
- For simple requests, create only the necessary tasks.
""",
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    response = generate_with_tools(
        messages = messages,
        tools=[]
    )

    content = response.choices[0].message.content

    try:
        plan = json.loads(content)

    except (json.JsonDecodeError, TypeError) as exc:
        raise ValueError(
            f"Planner returned invalid JSON:{content}"
        )from exc
    
    tasks = plan.get("tasks")

    if not isinstance(tasks, list) or not tasks:
        raise ValueError("planner must return a not empty task list.")

    for task in tasks:
        if not isinstance(task,dict):
            raise ValueError("Each task must be a JSON object.")

        if not isinstance(task.get("id"), int):
            raise ValueError("Each tast must have an integer id.")
        
        if not isinstance(task.get("description"),str) or not task["description"].strip():
            raise ValueError("Each task must have a description.")
        
        if task.get("status")!="pending":
            raise ValueError("Every new task must have status 'pending'.")
    return tasks

