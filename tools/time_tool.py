from datetime import datetime


def get_current_time() -> str:

    current_time = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    print(f"[TOOL] Current time: ({current_time})")
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")