from enum import Enum

class Direction(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1

    def __str__(self):
        if self == self.LEFT:
            return '-'
        elif self == self.RIGHT:
            return '+'
        else:
            return str(self.value)
