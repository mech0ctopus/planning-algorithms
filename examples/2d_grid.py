# Example 2.1: A robot moving on a 2D grid
#
# 10x10 Grid

from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace
from planning.search.abstract import StateTransitionFunction
from planning.search.search import ForwardSearchAlgorithm
import matplotlib.pyplot as plt


class MoveOnGrid(Action):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


common_actions = [MoveOnGrid(-1, 0),
                  MoveOnGrid(1, 0),
                  MoveOnGrid(0, -1),
                  MoveOnGrid(0, 1),
                  ]
                  

class GridStateTransitionFunction(StateTransitionFunction):
    def get_next_state(self, current_state: DiscreteState, action: Action,
                       state_space: DiscreteStateSpace) -> DiscreteState:      
        next_state_idx = (current_state.index[0] + action.x,
                          current_state.index[1] + action.y)
        return state_space.space[next_state_idx]

def build_state_space(xmax=10, ymax=10):
    state_space = DiscreteStateSpace()
    actions = [MoveOnGrid(-1, 0),
                MoveOnGrid(1, 0),
                MoveOnGrid(0, -1),
                MoveOnGrid(0, 1),
                ]
    # TODO: Set actions for states appropriately
    for x in range(xmax):
        for y in range (ymax):
            actions = []
            # Non-Border cells
            if 0 < x < (xmax - 1) and 0 < y < (ymax - 1):
                actions = common_actions
            else:
                state = DiscreteState(index=(x,y), actions=[])
            state = DiscreteState(index=(x,y), actions=actions)
            state_space.add_state(state)
    
    return state_space

def build_goal_space():
    goal_space = DiscreteStateSpace()
    goal_state = DiscreteState(index=(8,8), actions=common_actions)
    goal_space.add_state(goal_state)
    return goal_space

def build_xy_grid(state_space, xmax=10, ymax=10):
    grid = []
    for x in range(xmax):
        row = []
        for y in range(ymax):
            if state_space.space[(x,y)].is_visited():
                value = 1
            else:
                value = 0
            row.append(value)
        grid.append(row)
    return grid

if __name__ == '__main__':
    # Define State Space
    state_space = build_state_space()
    # Define Goal Space
    goal_space = build_goal_space()
    # Define StateTransitionFunction
    transition_func = GridStateTransitionFunction()
    # Define Initial State
    initial_state_idx = (2,2)
    initial_state = state_space.space[initial_state_idx]

    forward_search_on_2d_grid = ForwardSearchAlgorithm(state_space, transition_func,
                                                       initial_state, goal_space)
    result = forward_search_on_2d_grid.search()
    print(state_space)
    print(result)

    # Plot results
    grid = build_xy_grid(state_space)
    grid[2][2] = -1
    grid[8][8] = 2
    plt.imshow(grid, origin="lower")
    plt.savefig("2d_grid.png")