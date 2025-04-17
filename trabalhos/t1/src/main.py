from structures import *

def read_quintuple_machine_definition():
    quintuple_machine_definition = QuintupleTuringMachineDefinition(
        tapes=1,
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
        transitions=[],
        initial_state='A_'+ quintuple_machine_definition.initial_state,
        final_states=['A_' + quintuple_machine_definition.final_states[0]]
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
                    QuadrupleAct.read_write("B", quintuple_transition.source_state),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        m += 1

    return quadruple_machine_definition

if __name__ == '__main__':
    quintuple_machine_definition = read_quintuple_machine_definition()
    initial_state = list(input())

    quadruple_machine_definition = create_reversible_machine(quintuple_machine_definition)
    quadruple_machine_simulator = QuadrupleTuringMachineSimulator(quadruple_machine_definition)

    quadruple_machine_simulator.tapes[0].overwrite(initial_state)

    for transition in quadruple_machine_definition.transitions:
        print(transition)

    while True:
        if not quadruple_machine_simulator.step():
            break
    
    print(quadruple_machine_simulator.tapes[0].content)



