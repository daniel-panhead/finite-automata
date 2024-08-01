from dataclasses import dataclass
from typing import Generic, TypeVar


StateType = TypeVar("StateType")
InputType = TypeVar("InputType")


@dataclass
class TransitionFunction(Generic[StateType, InputType]):
    """
    Represents a transition function that takes a certain state and input
    and returns the next state that the FSA should advance to

    :param initial_state: initial state that the function will apply to
    :param input: input that the function will accept
    :param final_state: state that the FSA should advance to
    """
    initial_state: StateType
    input: InputType
    final_state: StateType
