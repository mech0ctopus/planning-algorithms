import unittest

from planning.space.primitives import DiscreteState
from planning.problems.five_state_problem import (
    AlphabetIndexIncrease,
    build_state_space,
    FiveLetterStateTransitionFunction,
)


class TestFiveStateProblem(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.transitions = FiveLetterStateTransitionFunction()
        self.space = build_state_space()

    def test_forward_transition_aa(self):
        state = DiscreteState(index='a')
        next_state = self.transitions.get_next_state(state,
                                                     AlphabetIndexIncrease(index=0),
                                                     self.space)
        self.assertEqual(next_state, DiscreteState(index='a'))

    def test_forward_transition_ab(self):
        state = DiscreteState(index='a')
        next_state = self.transitions.get_next_state(state,
                                                     AlphabetIndexIncrease(index=1),
                                                     self.space)
        self.assertEqual(next_state, DiscreteState(index='b'))

    def test_backward_transition_aa(self):
        state = DiscreteState(index='a')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=0),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='a'))

    def test_backward_transition_ac(self):
        state = DiscreteState(index='a')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=-2),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='c'))

    def test_backward_transition_ba(self):
        state = DiscreteState(index='b')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=1),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='a'))

    def test_backward_transition_cb(self):
        state = DiscreteState(index='c')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=1),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='b'))

    def test_backward_transition_cd(self):
        state = DiscreteState(index='c')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=-1),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='d'))

    def test_backward_transition_db(self):
        state = DiscreteState(index='d')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=2),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='b'))

    def test_backward_transition_dc(self):
        state = DiscreteState(index='d')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=1),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='c'))

    def test_backward_transition_ed(self):
        state = DiscreteState(index='e')
        previous_state = self.transitions.get_previous_state(state,
                                                             AlphabetIndexIncrease(index=1),
                                                             self.space)
        self.assertEqual(previous_state, DiscreteState(index='d'))



if __name__ == "__main__":
    unittest.main()
