import json

from llm.provider import generate_with_tools

from tools.calculator import calculate
from tools.time_tool import get_current_time
from tools.schemas import calculator_tool, time_tool
from agents.state import AgentState

TOOL_REGISTRY = {
    "calculate": calculate,
    "get_current_time": get_current_time,
}


def execute_tool(tool_call):
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    if tool_name not in TOOL_REGISTRY:
        return f"Unknown tool: {tool_name}"

    try:
        tool = TOOL_REGISTRY[tool_name]
        result = tool(**arguments)

        print(f"[TOOL RESULT] {result}")

        return result

    except Exception as e:
        error = f"Tool execution failed: {e}"

        print(f"[TOOL ERROR] {error}")

        return error


def run_agent(query: str) -> str:

    state = AgentState(
        messages = [
        {
            "role": "user",
            "content": query,
        }
    ]
    )



    for _ in range(5):

        state.steps+=1

        response = generate_with_tools(
            messages=state.messages,
            tools=[calculator_tool, time_tool],
        )

        message = response.choices[0].message

        # No tool requested → final answer
        if not message.tool_calls:
            print("\n[AGENT STATE]")
            print(f"Steps: {state.steps}")
            print(f"Tool calls: {state.tool_calls}")
            print(f"Errors: {state.errors}")
            return message.content

        # Add assistant's tool request to conversation history
        state.messages.append(
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

            state.tool_calls += 1

            result = execute_tool(tool_call)

            if isinstance(result, str) and result.startswith(
                "Tool execution failed:"
            ):
                state.errors +=1

            

            state.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "Agent stopped because the maximum number of steps was reached."