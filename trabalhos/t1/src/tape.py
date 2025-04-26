from typing import Any, List, Dict

from direction import Direction

class Tape:
    head: int
    content: Dict[int, Any]

    def __init__(self):
        self.head = 0
        self.content = {}

    def read(self) -> Any:
        return self.content.get(self.head, "B")

    def write(self, mark: Any):
        self.content[self.head] = mark

    def shift(self, direction: Direction):
        self.head += direction.value
    
    def overwrite(self, content: List[Any], offset: int = 0):
        self.content.clear()

        for i, mark in enumerate(content):
            self.content[i + offset] = mark
