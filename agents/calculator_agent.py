
import json

from llm.provider import generate_with_tools
from tools.calculator import calculate
from tools.schemas import calculator_tool


def run_calculator_agent(query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a calculator specialist. "
                "Use the calculate tool for arithmetic. "
                "Base your answer on the tool result. "
                "If the calculation fails, report the failure "
                "instead of inventing a result."
            ),
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    for _ in range(5):
        response = generate_with_tools(
            messages=messages,
            tools=[calculator_tool],
        )

        message = response.choices[0].message

        if not message.tool_calls:
            if not message.content:
                raise ValueError(
                    "Calculator agent returned an empty answer."
                )
            return message.content

        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        for call in message.tool_calls:
            if call.function.name != "calculate":
                raise ValueError(
                    f"Calculator agent cannot use {call.function.name}"
                )

            try:
                arguments = json.loads(call.function.arguments)
                result = calculate(**arguments)
                tool_content = json.dumps(
                    {"ok": True, "result": result}
                )
            except Exception as exc:
                tool_content = json.dumps(
                    {"ok": False, "error": str(exc)}
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": tool_content,
                }
            )

    raise RuntimeError(
        "Calculator agent exceeded its iteration limit."
    )
