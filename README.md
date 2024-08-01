# Finite-State Machine (FSM) Library

This library can be used to generate finite-state automata.

## Example Usage

```python
from finite_automaton import FiniteAutomaton, TransitionFunction

fsa = FiniteAutomaton(
    {"S0", "S1", "S2"},
    {0, 1},
    "S0",
    {"S0", "S1", "S2"},
    [
        TransitionFunction("S0", 0, "S0"),
        TransitionFunction("S0", 1, "S1"),
        TransitionFunction("S1", 0, "S2"),
        TransitionFunction("S1", 1, "S0"),
        TransitionFunction("S2", 0, "S1"),
        TransitionFunction("S2", 1, "S2"),
    ],
)

assert fsa.current_state == "S0"

fsa.input(1)
assert fsa.current_state == "S1"
assert fsa.in_final_state()

fsa.input(1)
assert fsa.current_state == "S0"
assert fsa.in_final_state()

fsa.input(0)
assert fsa.current_state == "S0"
assert fsa.in_final_state()
```
