

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Any, Self

import math
import re

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

@dataclass(eq=True)
class State:
    id: int
    label: str

@dataclass
class QuintupleAct:
    read: Any
    write: Any
    direction: Direction

@dataclass
class QuintupleTransition:
    source_state: int
    destination_state: int
    acts: List[QuintupleAct]

    def parse(line: str) -> Self:
        p = re.compile(r'\((?P<source>\d+),(?P<read>.+)\)=\((?P<destination>\d+),(?P<write>.+),(?P<shift>[RLS])\)')
        match = p.match(line)

        if not match:
            raise ValueError(f"Invalid quintuple format: {line}")
        
        source_state = match.group("source")
        read_symbol = match.group("read")
        destination_state = match.group("destination")
        write_symbol = match.group("write")
        shift = match.group("shift")

        direction_map = {
            'L': Direction.LEFT,
            'R': Direction.RIGHT,
            'S': Direction.STAY
        }

        return QuintupleTransition(
            source_state=source_state,
            destination_state=destination_state,
            acts=[
                QuintupleAct(
                    read=read_symbol,
                    write=write_symbol,
                    direction=direction_map[shift]
                )
            ]
        )

class QuadrupleActType(Enum):
    SHIFT = auto()
    READ_WRITE = auto()

@dataclass
class QuadrupleAct:
    kind: QuadrupleActType
    direction: Optional[Direction] = None
    read: Optional[Any] = None
    write: Optional[Any] = None

    def shift(direction: Direction):
        return QuadrupleAct(
            kind=QuadrupleActType.SHIFT,
            direction=direction
        )
    
    def read_write(read: Any, write: Any):
        return QuadrupleAct(
            kind=QuadrupleActType.READ_WRITE,
            read=read,
            write=write
        )

@dataclass
class QuadrupleTransition:
    source_state: str
    destination_state: str
    acts: List[QuadrupleAct]

    def matches(self, state: str, data: List[Any]) -> bool:
        if self.source_state != state:
            return False

        for i, act in enumerate(self.acts):
            if act.kind == QuadrupleActType.READ_WRITE and act.read != data[i]:
                return False

        return True
    
    def __str__(self):
        inputs = []
        outputs = []
        
        for act in self.acts:
            if act.kind == QuadrupleActType.SHIFT:
                inputs.append('/')
                outputs.append(str(act.direction))
            elif act.kind == QuadrupleActType.READ_WRITE:
                inputs.append(str(act.read))
                outputs.append(str(act.write))
        
        result = self.source_state
        result += f'[{" ".join(inputs)}]'
        result += ' -> '
        result += f'[{" ".join(outputs)}]'
        result += self.destination_state

        return result
    
@dataclass
class QuintupleTuringMachineDefinition:
    tapes: int
    alphabet: List[Any]
    transitions: List[QuintupleTransition]
    initial_state: str
    final_states: List[str]

@dataclass
class QuadrupleTuringMachineDefinition:
    tapes: int
    alphabet: List[Any]
    transitions: List[QuadrupleTransition]
    initial_state: str
    final_states: List[str]

    def find_matching_transition(self, state: str, data: List[Any]) -> Optional[QuadrupleTransition]:
        for transition in self.transitions:
            if transition.matches(state, data):
                return transition

        return None

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
    
    def overwrite(self, content: List[Any]):
        self.content.clear()

        for i, mark in enumerate(content):
            self.content[i] = mark

class QuadrupleTuringMachineSimulator:
    definition: QuadrupleTuringMachineDefinition

    tapes: List[Tape]
    current_state: str

    def __init__(self, definition: QuadrupleTuringMachineDefinition):
        self.tapes = [Tape() for _ in range(definition.tapes)]

        self.definition = definition
        self.current_state = definition.initial_state
    
    def run(self, max_steps=math.inf) -> None:
        current_step = 0

        while current_step < max_steps:
            if not self.step():
                return True

            current_step += 1
        
        return False
    
    def step(self):
        heads = [tape.head for tape in self.tapes]
        transition = self.find_next_transition()

        if transition is None:
            return False

        for i, act in enumerate(transition.acts):
            if act.kind == QuadrupleActType.READ_WRITE:
                self.tapes[i].write(act.write)
            elif act.kind == QuadrupleActType.SHIFT:
                self.tapes[i].shift(act.direction)
        
        self.current_state = transition.destination_state

        return True
    
    def find_next_transition(self) -> Optional[QuadrupleTransition]:
        data = [tape.read() for tape in self.tapes]
        return self.definition.find_matching_transition(self.current_state, data)
    
    def has_halted(self) -> bool:
        return self.has_accepted() or self.has_rejected()
    
    def has_accepted(self) -> bool:
        return self.current_state in self.definition.final_states
    
    def has_rejected(self) -> bool:
        if self.has_accepted():
            return False
        
        data = [tape.read() for tape in self.tapes]

        return self.definition.find_matching_transition(self.current_state, data) is None
