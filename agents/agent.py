import json

from llm.provider import generate_with_tools
from tools.calculator import calculate
from tools.schemas import calculator_tool


TOOL_REGISTRY = {
    "calculate": calculate,
}


def run_agent(query: str) -> str:
    messages = [
        {
            "role": "user",
            "content": query,
        }
    ]

    for _ in range(5):
        response = generate_with_tools(
            messages=messages,
            tools=[calculator_tool],
        )

        message = response.choices[0].message

        # No tool requested → final answer
        if not message.tool_calls:
            return message.content

        # Add the assistant's tool request to conversation history
        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ],
            }
        )

        # Execute requested tools
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name not in TOOL_REGISTRY:
                result = f"Unknown tool: {tool_name}"
            else:
                try:
                    tool = TOOL_REGISTRY[tool_name]
                    result = tool(**arguments)
                except Exception as e:
                    result = f"Tool execution failed: {e}"

            # Send tool result back to LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "Agent stopped because the maximum number of steps was reached."