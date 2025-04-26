from typing import Any, Self, List
from dataclasses import dataclass
import re

from direction import Direction

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

        direction_lookup = {
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
                    direction=direction_lookup[shift]
                )
            ]
        )
    
@dataclass
class QuintupleTuringMachineDefinition:
    tapes: int
    alphabet: List[Any]
    transitions: List[QuintupleTransition]
    initial_state: str
    final_states: List[str]
