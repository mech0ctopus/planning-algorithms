# Example 2.1: A robot moving on a 2D grid
#
# 10x10 Grid

from planning.search.primitives import Action, DiscreteState, DiscreteStateSpace
from planning.search.abstract import StateTransitionFunction
from planning.search.search import ForwardSearchAlgorithm


class MoveOnGrid(Action):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class GridStateTransitionFunction(StateTransitionFunction):
    def get_next_state(self, current_state: DiscreteState, action: Action,
                       state_space: DiscreteStateSpace) -> DiscreteState:
        next_state_x_idx = current_state.index[0] + action.x
        next_state_y_idx = current_state.index[1] + action.y
        return state_space.space(next_state_x_idx,
                                 next_state_y_idx)


def build_state_space():
    state_space = DiscreteStateSpace()
    common_actions = [MoveOnGrid(-1, 0),
                      MoveOnGrid(1, 0),
                      MoveOnGrid(0, -1),
                      MoveOnGrid(0, 1),
                      ]
    for x in range(10):
        for y in range (10):
            state = DiscreteState(index=(x,y), actions=common_actions)
            state_space.add_state(state)
    return state_space

def build_goal_space():
    goal_space = DiscreteStateSpace()
    goal_state = DiscreteState(index=(8,8))
    goal_space.add_state(goal_state)
    return goal_space

if __name__ == '__main__':
    # Define State Space
    state_space = build_state_space()
    # Define Goal Space
    goal_space = build_goal_space()
    # Define StateTransitionFunction
    transition_func = GridStateTransitionFunction()
    # Define Initial State
    initial_state = state_space.space[(0,0)]

    forward_search_on_2d_grid = ForwardSearchAlgorithm()
    forward_search_on_2d_grid.search()