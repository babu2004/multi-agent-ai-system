from llm.provider import generate_with_tools
from tools.schemas import calculator_tool


messages = [
    {
        "role": "user",
        "content": "What is 125 multiplied by 37?"
    }
]


response = generate_with_tools(
    messages=messages,
    tools=[calculator_tool]
)

print(response.choices[0].message)