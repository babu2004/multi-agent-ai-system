calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform basic arithmetic using two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                },
                "operation": {
                    "type": "string",
                    "enum": ["+", "-", "*", "/"],
                    "description": "Arithmetic operation"
                }
            },
            "required": ["a", "b", "operation"]
        }
    }
}