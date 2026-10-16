from dataclasses import dataclass, field

@dataclass

class AgentState:
    messages: list = field(default_factory=list)
    steps: int=0
    tool_calls:int=0
    errors:int=0
    plan: list[dict] = field(default_factory=list)
    task_results: dict[int, str] = field(default_factory=dict)

    def complete_task(self, task_id:int, result: str)->None:
        for task in self.plan:
            if task["id"]==task_id:
                task["status"]="completed"
                self.task_results[task_id]=str(result)
                return 
            
        raise ValueError(f"Task ID {task_id} not found in plan")

    def fail_task(self, task_id:int, error: str)-> None:
        for task in self.plan:
            if task["id"] == task_id:
                task["status"] = "Failed"
                self.task_results[task_id] = str(error)
                return 
        raise ValueError(f"Task ID {task_id} not found in plan")
