import pytest

from finite_automaton import FSAException, FiniteAutomaton, TransitionFunction


@pytest.fixture
def basic_fsa():
    fsa = FiniteAutomaton(
        {"S0", "S1"},
        {0, 1},
        "S0",
        {"S1"},
        [
            TransitionFunction("S0", 0, "S1"),
            TransitionFunction("S0", 1, "S0"),
        ],
    )
    return fsa


@pytest.fixture
def mod_three_fsa():
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
    return fsa


class TestFiniteAutomaton:
    def test_basic_fsa(self, basic_fsa: FiniteAutomaton[str, int]):
        assert basic_fsa.current_state == "S0"
        assert not basic_fsa.in_final_state()

        basic_fsa.input(1)

        assert basic_fsa.current_state == "S0"
        assert not basic_fsa.in_final_state()

        basic_fsa.input(0)

        assert basic_fsa.current_state == "S1"
        assert basic_fsa.in_final_state()

    def test_mod_three_110(self, mod_three_fsa: FiniteAutomaton[str, int]):
        assert mod_three_fsa.current_state == "S0"

        mod_three_fsa.input(1)
        assert mod_three_fsa.current_state == "S1"
        assert mod_three_fsa.in_final_state()

        mod_three_fsa.input(1)
        assert mod_three_fsa.current_state == "S0"
        assert mod_three_fsa.in_final_state()

        mod_three_fsa.input(0)
        assert mod_three_fsa.current_state == "S0"
        assert mod_three_fsa.in_final_state()

    def test_mod_three_1010(self, mod_three_fsa: FiniteAutomaton[str, int]):
        assert mod_three_fsa.current_state == "S0"

        mod_three_fsa.input(1)
        assert mod_three_fsa.current_state == "S1"
        assert mod_three_fsa.in_final_state()

        mod_three_fsa.input(0)
        assert mod_three_fsa.current_state == "S2"
        assert mod_three_fsa.in_final_state()

        mod_three_fsa.input(1)
        assert mod_three_fsa.current_state == "S2"
        assert mod_three_fsa.in_final_state()

        mod_three_fsa.input(0)
        assert mod_three_fsa.current_state == "S1"
        assert mod_three_fsa.in_final_state()


class TestFiniteAutomatonExceptions:
    def test_accepting_states_not_subset(self):
        with pytest.raises(
            FSAException, match="Accepting states must be a subset of all states"
        ):
            FiniteAutomaton(
                {"S0", "S1"},
                {0, 1},
                "S0",
                {"S1", "S2"},
                [TransitionFunction("S0", 0, "S1"), TransitionFunction("S0", 1, "S0")],
            )

    def test_initial_state_not_member(self):
        with pytest.raises(FSAException, match="Initial state must be in all states"):
            FiniteAutomaton(
                {"S0", "S1"},
                {0, 1},
                "S2",
                {"S1"},
                [TransitionFunction("S0", 0, "S1"), TransitionFunction("S0", 1, "S0")],
            )

    def test_transition_initial_not_member(self):
        with pytest.raises(
            FSAException, match="Transition initial state must be in all states"
        ):
            FiniteAutomaton(
                {"S0", "S1"},
                {0, 1},
                "S0",
                {"S1"},
                [TransitionFunction("S2", 0, "S1"), TransitionFunction("S0", 1, "S0")],
            )

    def test_transition_final_not_member(self):
        with pytest.raises(
            FSAException, match="Transition final state must be in all states"
        ):
            FiniteAutomaton(
                {"S0", "S1"},
                {0, 1},
                "S0",
                {"S1"},
                [TransitionFunction("S0", 0, "S1"), TransitionFunction("S0", 1, "S2")],
            )

    def test_initial_transition_input_not_member(self):
        with pytest.raises(
            FSAException, match="Transition input must be in input alphabet"
        ):
            FiniteAutomaton(
                {"S0", "S1"},
                {0, 1},
                "S0",
                {"S1"},
                [TransitionFunction("S0", 0, "S1"), TransitionFunction("S0", 2, "S0")],
            )

    def test_duplicate_transitions(self):
        with pytest.raises(
            FSAException,
            match="Transition functions must have unique combo of initial state and input",
        ):
            FiniteAutomaton(
                {"S0", "S1"},
                {0, 1},
                "S0",
                {"S1"},
                [TransitionFunction("S0", 0, "S1"), TransitionFunction("S0", 0, "S0")],
            )

    def test_transition_input_not_member(self, basic_fsa: FiniteAutomaton[str, int]):
        basic_fsa.input(1)
        with pytest.raises(
            FSAException,
            match="Combination of current state and input was not found in transitions list",
        ):
            basic_fsa.input(2)
