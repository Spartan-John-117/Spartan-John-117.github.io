from typing import Any


def run_turing_machine(
        machine: dict[str, Any],
        input_: str,
        steps: int | None = None,
) -> tuple[str, list, bool]:
    blank = machine["blank"]
    table = machine["table"]
    state = machine["start state"]
    final_states = machine["final states"]

    memory = list(input_)
    position = 0
    history = []
    accepted = False
    step_count = 0

    while True:
        if state in final_states:
            accepted = True
            break
        if steps is not None and step_count >= steps:
            break
        step_count += 1

        reading = memory[position]
        current_transition = table[state]
        transition = current_transition[reading]
        if transition is None:
            break

        history.append({
            "state": state,
            "reading": reading,
            "position": position,
            "memory": "".join(memory),
            "transition": transition,
        })
        
        if type(transition) == str:
            direction = transition
        else:
            direction = "R" if "R" in transition else "L"
            if "write" in transition:
                memory[position] = transition["write"]
            state = transition[direction]

        if direction == "R":
            position += 1
        else:
            position -= 1

        if position < 0:
            memory.insert(0, blank)
            position = 0
        elif position > len(memory) - 1:
            memory.append(blank)
            position = len(memory) - 1

    while memory and memory[0] == blank:
        memory.pop(0)
    while memory and memory[-1] == blank:
        memory.pop()

    return "".join(memory), history, accepted