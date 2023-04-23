from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace
from planning.search.abstract import SearchProblem, StateTransitionFunction
from typing import List

LETTERS = 'abcde'


class AlphabetIndexIncrease(Action):
    def __init__(self, index) -> None:
        self.index = index


class FiveLetterStateTransitionFunction(StateTransitionFunction):
    def get_next_state(self, current_state: DiscreteState, action: AlphabetIndexIncrease,
                       state_space: DiscreteStateSpace) -> DiscreteState:      
        next_letter_idx = LETTERS.find(current_state.index) + action.index
        return state_space.space[LETTERS[next_letter_idx]]

    def get_previous_state(self, future_state: DiscreteState, action: AlphabetIndexIncrease,
                           state_space: DiscreteStateSpace) -> DiscreteState:
        previous_letter_idx = LETTERS.find(future_state.index) - action.index
        return state_space.space[LETTERS[previous_letter_idx]]


class FiveStateSearchProblem(SearchProblem):
    def get_actions(self, state: DiscreteState) -> List[Action]:
        if state.index == 'a':
            return [AlphabetIndexIncrease(index=0),
                    AlphabetIndexIncrease(index=1)]
        elif state.index == 'b':
            return [AlphabetIndexIncrease(index=1),
                    AlphabetIndexIncrease(index=2)]
        elif state.index == 'c':
            return [AlphabetIndexIncrease(index=1),
                    AlphabetIndexIncrease(index=-2)]
        elif state.index == 'd':
            return [AlphabetIndexIncrease(index=-1),
                    AlphabetIndexIncrease(index=1)]
        elif state.index == 'e':
            return []
        else:
            raise ValueError(f"Unknown state index: {state.index}")

    def get_previous_actions(self, state: DiscreteState) -> List[Action]:
        if state.index == 'a':
            return [AlphabetIndexIncrease(index=0),
                    AlphabetIndexIncrease(index=-2)]
        elif state.index == 'b':
            return [AlphabetIndexIncrease(index=1)]
        elif state.index == 'c':
            return [AlphabetIndexIncrease(index=1),
                    AlphabetIndexIncrease(index=-1)]
        elif state.index == 'd':
            return [AlphabetIndexIncrease(index=2),
                    AlphabetIndexIncrease(index=1)]
        elif state.index == 'e':
            return [AlphabetIndexIncrease(index=1)]
        else:
            raise ValueError(f"Unknown state index: {state.index}")

def build_state_space():
    state_space = DiscreteStateSpace()
    state_space.add_state(DiscreteState(index='a'))
    state_space.add_state(DiscreteState(index='b'))
    state_space.add_state(DiscreteState(index='c'))
    state_space.add_state(DiscreteState(index='d'))
    state_space.add_state(DiscreteState(index='e'))
    return state_space

def build_goal_space(goal_state_index):
    goal_space = DiscreteStateSpace()
    goal_state = DiscreteState(index=goal_state_index)
    goal_space.add_state(goal_state)
    return goal_space

def build_problem(initial_state_index, goal_state_index):
    # Define search problem
    state_space = build_state_space()
    problem = FiveStateSearchProblem(state_space=state_space,
                                  goal_space=build_goal_space(goal_state_index),
                                  transition_function=FiveLetterStateTransitionFunction(),
                                  initial_state=state_space.space[initial_state_index]
                                  )
    return state_space, problem
