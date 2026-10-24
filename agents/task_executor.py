import json

from llm.provider import generate_with_tools
from tools.schemas import calculator_tool, time_tool
from tools.calculator import calculate
from tools.time_tool import get_current_time

TOOL_REGISTRY = {
    "calculate": calculate,
    "get_current_time": get_current_time
}

AVAILABLE_TOOLS = [calculator_tool,time_tool]

def execute_task(description: str,task_results:dict[int, str])-> str:
    previous_results = "\n ".join(
        f"Task {task_id} result: {result}"
        for task_id , result in task_results.items()
    )

    messages = [
        {
            "role":"system",
            "content":(
                "execute the assigned task using the available tools when needed. "
                "previous tool results are given as content."
                "Do not claim a tool operation succeeded unless its result confirms it. "
                "If a tool fails, explain the failure rather than inventing a result."
            ),
        },

        {
            "role":"user",
            "content":(
                f"Task: {description}\n\n"
                f"Previous results:\n{previous_results or 'None'}"
            ),
        },
    ]

    for _ in range(5):
        response = generate_with_tools(
            messages = messages,
             tools = AVAILABLE_TOOLS
        )
        message = response.choices[0].message

        if not message.tool_calls:
            if not message.content:
                raise ValueError("The model returned a empty task result.")
            return message.content

        messages.append(
            {
                "role":"assistant",
                "content":message.content,
                "tool_calls":[
                    {
                        "id":call.id,
                        "type":"function",
                        "function":{
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        for call in message.tool_calls:
            name = call.function.name

            try:
                arguments = json.loads(call.function.arguments)
                tool = TOOL_REGISTRY.get(name)

                if tool is None:
                    raise ValueError(f"Unknown tool: {name}")

                result = tool(**arguments)

                tool_content = json.dumps(
                    {"ok": True, "result": result},
                    default=str,
                )

            except Exception as exc:
                raise RuntimeError(
                    f"Tool '{name}' execution failed: {exc}"
                ) from exc
            messages.append(
                {
                    "role":"tool",
                    "tool_call_id": call.id,
                    "content":tool_content,
                }
            )
    raise RuntimeError("Task exceeded the maximum number of LLM Iteratiions.")
