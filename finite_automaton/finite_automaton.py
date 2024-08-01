from typing import Generic
from .states import InputType, StateType, TransitionFunction


class FSAException(Exception):
    pass


class FiniteAutomaton(Generic[StateType, InputType]):
    def __init__(
        self,
        all_states: set[StateType],
        input_alphabet: set[InputType],
        initial_state: StateType,
        accepting_states: set[StateType],
        transitions: list[TransitionFunction[StateType, InputType]],
    ) -> None:
        """Make a new finite state automata.

        :param all_states: a set of all possible states for the FSA.
        :param input_alphabet: a set of all possible inputs for the FSA.
        :param initial_state: initial state of the FSA. Must be a member of `all_states`.
        :param accepting_states: a set of all accepting/final states. Must be a subset of `all_states`.
        :param transitions: list of `TransitionFunction` that define how inputs change the FSA state.

        :raises FSAException: raises error if parameters do not satisfy member/subset/uniqueness requirements.
        """
        self._check_fsa_params(
            all_states, input_alphabet, initial_state, accepting_states, transitions
        )

        self._all_states = all_states
        self._input_alphabet = input_alphabet
        self._initial_state = initial_state
        self._accepting_states = accepting_states
        self._transitions = {(tr.initial_state, tr.input): tr for tr in transitions}

        self.current_state = initial_state

    def _check_fsa_params(
        self,
        all_states: set[StateType],
        input_alphabet: set[InputType],
        initial_state: StateType,
        accepting_states: set[StateType],
        transitions: list[TransitionFunction[StateType, InputType]],
    ):
        """Checks that parameters for FSA satisfy all requirements"""
        if not accepting_states.issubset(all_states):
            raise FSAException("Accepting states must be a subset of all states")
        if initial_state not in all_states:
            raise FSAException("Initial state must be in all states")

        existing_transitions: set[tuple[StateType, InputType]] = set()
        for tr in transitions:
            if tr.initial_state not in all_states:
                raise FSAException("Transition initial state must be in all states")
            if tr.final_state not in all_states:
                raise FSAException("Transition final state must be in all states")
            if tr.input not in input_alphabet:
                raise FSAException("Transition input must be in input alphabet")
            uniq_tuple = (tr.initial_state, tr.input)
            if uniq_tuple in existing_transitions:
                raise FSAException(
                    "Transition functions must have unique combo of initial state and input"
                )
            existing_transitions.add(uniq_tuple)

    def input(self, input: InputType):
        """Give an input to the FSA.

        :param input: input to pass to the FSA - must be a member of the input alphabet set
        :raises FSAException: raises exception if the combination of current state/input is not found in the list of transitions
        """
        tr = self._transitions.get((self.current_state, input))
        if tr is None:
            raise FSAException(
                "Combination of current state and input was not found in transitions list"
            )

        self.current_state = tr.final_state

    def in_final_state(self):
        """Returns True if the FSA is currently in an accepting/final state."""
        return self.current_state in self._accepting_states
