from structures import *
from gui import *

def read_quintuple_machine_definition():
    quintuple_machine_definition = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=[],
        transitions=[],
        initial_state="",
        final_states=[]
    )

    size_parameters = map(int, input().split())

    number_of_states = next(size_parameters)
    number_of_input_symbols = next(size_parameters)
    number_of_tape_symbols = next(size_parameters)
    number_of_transitions = next(size_parameters)

    states = list(input().split())

    quintuple_machine_definition.initial_state = states[0]
    quintuple_machine_definition.final_states = states[-1]
    
    input_symbols = input()
    tape_symbols = input()

    quintuple_machine_definition.alphabet = list(tape_symbols)

    for _ in range(number_of_transitions):
        quintuple_machine_definition.transitions.append(QuintupleTransition.parse(input()))
    
    return quintuple_machine_definition

def create_reversible_machine(quintuple_machine_definition: QuintupleTuringMachineDefinition):
    if quintuple_machine_definition.tapes != 1:
        raise ValueError("Reversible machines only support one tape.")
    
    if len(quintuple_machine_definition.final_states) != 1:
        raise ValueError("Reversible machines only support one final state.")
    
    quadruple_machine_definition = QuadrupleTuringMachineDefinition(
        tapes=3,
        alphabet=[],
        transitions=[],
        initial_state='A_'+ quintuple_machine_definition.initial_state,
        final_states=['C_'+ quintuple_machine_definition.initial_state]
    )

    m = 1

    for quintuple_transition in quintuple_machine_definition.transitions:
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="A_" + quintuple_transition.source_state,
                destination_state="A'_" + str(m),
                acts=[
                    QuadrupleAct.read_write(quintuple_transition.acts[0].read, quintuple_transition.acts[0].write),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write("B", "B"),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="A'_" + str(m),
                destination_state="A_" + quintuple_transition.destination_state,
                acts=[
                    QuadrupleAct.shift(quintuple_transition.acts[0].direction),
                    QuadrupleAct.read_write("B", m),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        # C states (retrace)
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="C_" + quintuple_transition.destination_state,
                destination_state="C'_" + str(m),
                acts=[
                    QuadrupleAct.shift(Direction(-quintuple_transition.acts[0].direction.value)),
                    QuadrupleAct.read_write(m, "B"),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="C'_" + str(m),
                destination_state="C_" + quintuple_transition.source_state,
                acts=[
                    QuadrupleAct.read_write(quintuple_transition.acts[0].write, quintuple_transition.acts[0].read),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write("B", "B"),
                ]
            )
        )

        m += 1

    # B states (copy output)
    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state="A_"+quintuple_machine_definition.final_states[0],
            destination_state="B'_1",
            acts=[
                QuadrupleAct.read_write("B", "B"),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.read_write("B", "B"),
            ]
        )
    )

    for tape_symbol in quintuple_machine_definition.alphabet:
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="B_1",
                destination_state=("B'_1" if tape_symbol != "B"
                    else "B'_2"),
                acts=[
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("B", tape_symbol),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="B_2",
                destination_state=("B'_2" if tape_symbol != "B"
                    else "C_" + quintuple_machine_definition.final_states[0]),
                acts=[
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                ]
            )
        )

    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state="B'_1",
            destination_state="B_1",
            acts=[
                QuadrupleAct.shift(Direction.RIGHT),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.shift(Direction.RIGHT),
            ]
        )
    )

    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state="B'_2",
            destination_state="B_2",
            acts=[
                QuadrupleAct.shift(Direction.LEFT),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.shift(Direction.LEFT),
            ]
        )
    )

    #for transition in quadruple_machine_definition.transitions:
    #    print(transition)

    return quadruple_machine_definition

# def print_tape(tape: Tape, start: int, end: int):
#     size = end - start
    
#     head_line = ""
#     content_line = ""

#     for i in range(start, end):
#         head_line += ('v' if tape.head == i else " ").rjust(3)
#         content_line += str(tape.content.get(i, 'B')).rjust(3)
    
#     print(head_line)
#     print(content_line)

def print_tape(tape: Tape, start: int, end: int):
    size = end - start
    
    head_line = ""
    content_line = ""

    for i in range(start, end):
        mark = '*' if tape.head == i else " "
        mark += str(tape.content.get(i, 'B'))
        content_line += mark.rjust(4)

    
    print(content_line)

# def print_tape(tape: Tape, start: int, end: int):
#     size = end - start
    
#     head_line = ''
#     content_line = ['|']

#     for i in range(start, end):
#         mark = str(tape.content.get(i, 'B'))

#         content_line.append(mark.rjust(4))
#         content_line.append('|')
    
#     if tape.head >= start and tape.head < end:
#         relative = (tape.head - start) * 2
        
#         content_line[relative] = '['
#         content_line[relative + 2] = ']'

    
#     print(''.join(content_line))

if __name__ == '__main__':
    quintuple_machine_definition = read_quintuple_machine_definition()
    initial_state = list(input())

    quadruple_machine_definition = create_reversible_machine(quintuple_machine_definition)
    quadruple_machine_simulator = QuadrupleTuringMachineSimulator(quadruple_machine_definition)

    quadruple_machine_simulator.tapes[0].overwrite(initial_state)

    gui = TuringMachineGUI(quadruple_machine_simulator, quadruple_machine_definition.transitions)
    gui.run()
    




