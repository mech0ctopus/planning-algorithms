# Example 2.1: A robot moving on a 2D grid
#
# 10x10 Grid

from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace
from planning.search.abstract import StateTransitionFunction
from planning.search.search import BreadthFirstForwardSearchAlgorithm
import matplotlib.pyplot as plt
import numpy as np

# TODO: Resolve zero-index / one-index issue. Plot is off by 1 spot in X and Y
# TODO: Cleanup / Refactor this example. Create an abstract PlanningProblemClass?

XMAX = 15
YMAX = 15
INITIAL_STATE_IDX = (1,2)
GOAL_STATE_IDX = (8,5)

class MoveOnGrid(Action):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

COMMON_ACTIONS = [MoveOnGrid(-1, 0),
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


def build_state_space():
    state_space = DiscreteStateSpace()
    for x in range(XMAX):
        for y in range (YMAX):
            # Non-Border cells
            if 0 < x < (XMAX - 1) and 0 < y < (YMAX - 1):
                actions = COMMON_ACTIONS
            else:
                actions = []
                if x == 0:
                    actions.append(MoveOnGrid(1, 0))
                if y == 0:
                    actions.append(MoveOnGrid(0, 1))
                if x == XMAX:
                    actions.append(MoveOnGrid(-1, 0))
                if y == YMAX:
                    actions.append(MoveOnGrid(0, -1))

            state = DiscreteState(index=(x,y), actions=actions)
            state_space.add_state(state)
    
    return state_space

def build_goal_space():
    goal_space = DiscreteStateSpace()
    goal_state = DiscreteState(index=GOAL_STATE_IDX, actions=COMMON_ACTIONS)
    goal_space.add_state(goal_state)
    return goal_space

def build_xy_grid(state_space):
    grid = np.zeros((XMAX, YMAX))
    for x in range(XMAX):
        for y in range(YMAX):
            grid[x, y] = state_space.space[(x,y)].is_visited()
    return grid

def plot_results(state_space, plan):
    grid = build_xy_grid(state_space)

    for state_idx in plan:
        grid[state_idx[0]][state_idx[1]] = 3

    grid[INITIAL_STATE_IDX[0]][INITIAL_STATE_IDX[1]] = -1
    grid[GOAL_STATE_IDX[0]][GOAL_STATE_IDX[1]] = 2

    plt.imshow(grid.T, origin="lower")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("2d_grid.png")

if __name__ == '__main__':
    # Define State Space
    state_space = build_state_space()
    # Define Goal Space
    goal_space = build_goal_space()
    # Define StateTransitionFunction
    transition_func = GridStateTransitionFunction()
    # Define Initial State
    initial_state = state_space.space[INITIAL_STATE_IDX]

    # Solve search problem
    forward_search_on_2d_grid = BreadthFirstForwardSearchAlgorithm(state_space, transition_func,
                                                                   initial_state, goal_space,
                                                                   verbose=False)
    success = forward_search_on_2d_grid.search()
    print(f"Success: {success}")
    # Get Plan
    plan = forward_search_on_2d_grid.get_plan()

    # Print / Plot results
    print("Plan:")
    for state_idx in plan:
        print(state_idx)
    plot_results(state_space, plan)
