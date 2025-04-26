from typing import Any

def format_mark(mark: Any) -> str:
    if isinstance(mark, int):
        return f"#{mark}"
    
    return mark
