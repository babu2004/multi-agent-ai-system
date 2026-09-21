from dataclasses import dataclass, field

@dataclass

class AgentState:
    messages: list = field(default_factory=list)
    steps: int=0
    tool_calls:int=0
    errors:int=0



