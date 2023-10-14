# Example 2.1: A robot moving on a 2d grid

from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace
from planning.search.abstract import SearchProblem, StateTransitionFunction
import matplotlib.pyplot as plt
import numpy as np
from typing import List

# TODO: Resolve zero-index / one-index issue. Plot is off by 1 spot in X and Y
# TODO: Cleanup / Refactor this into a class.
XMAX = 15
YMAX = 15


class MoveOn2dGrid(Action):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.cost = 1


class GridStateTransitionFunction(StateTransitionFunction):
    def get_next_state(self, current_state: DiscreteState, action: MoveOn2dGrid,
                       state_space: DiscreteStateSpace) -> DiscreteState:
        next_state_idx = (current_state.index[0] + action.x,
                          current_state.index[1] + action.y)
        return state_space.space[next_state_idx]

    def get_previous_state(self, future_state: DiscreteState, action: MoveOn2dGrid,
                           state_space: DiscreteStateSpace) -> DiscreteState:
        previous_state_idx = (future_state.index[0] - action.x,
                              future_state.index[1] - action.y)
        return state_space.space[previous_state_idx]


class Grid2dSearchProblem(SearchProblem):
    def get_actions(self, state: DiscreteState) -> List[Action]:
        x, y = state.index
        # Non-Border cells
        if 0 < x < (XMAX - 1) and 0 < y < (YMAX - 1):
            actions = [MoveOn2dGrid(-1, 0),
                       MoveOn2dGrid(1, 0),
                       MoveOn2dGrid(0, -1),
                       MoveOn2dGrid(0, 1),
                       ]
        else:
            actions = []
            if x == 0:
                actions.append(MoveOn2dGrid(1, 0))
            if y == 0:
                actions.append(MoveOn2dGrid(0, 1))
            if x == XMAX:
                actions.append(MoveOn2dGrid(-1, 0))
            if y == YMAX:
                actions.append(MoveOn2dGrid(0, -1))
        return actions

    def get_previous_actions(self, state: DiscreteState) -> List[Action]:
        x, y = state.index
        # Non-Border cells
        if 0 < x < (XMAX - 1) and 0 < y < (YMAX - 1):
            actions = [MoveOn2dGrid(-1, 0),
                       MoveOn2dGrid(1, 0),
                       MoveOn2dGrid(0, -1),
                       MoveOn2dGrid(0, 1),
                       ]
        else:
            actions = []
            if x == 0:
                actions.append(MoveOn2dGrid(-1, 0))
            if y == 0:
                actions.append(MoveOn2dGrid(0, -1))
            if x == XMAX:
                actions.append(MoveOn2dGrid(1, 0))
            if y == YMAX:
                actions.append(MoveOn2dGrid(0, 1))
        return actions


def build_state_space():
    state_space = DiscreteStateSpace()
    for x in range(XMAX):
        for y in range(YMAX):
            state = DiscreteState(index=(x, y))
            state_space.add_state(state)
    return state_space


def build_goal_space(goal_state_index):
    goal_space = DiscreteStateSpace()
    goal_state = DiscreteState(index=goal_state_index)
    goal_space.add_state(goal_state)
    return goal_space


def build_xy_grid(state_space):
    grid = np.zeros((XMAX, YMAX))
    for x in range(XMAX):
        for y in range(YMAX):
            grid[x, y] = state_space.space[(x, y)].is_visited()
    return grid


def build_problem(initial_state_index, goal_state_index):
    # Define search problem
    state_space = build_state_space()
    problem = Grid2dSearchProblem(state_space=state_space,
                                  goal_space=build_goal_space(goal_state_index),
                                  transition_function=GridStateTransitionFunction(),
                                  initial_state=state_space.space[initial_state_index]
                                  )
    return state_space, problem


def plot_results(problem, plan, initial_state_index, goal_state_index):
    grid = build_xy_grid(problem.state_space)

    for state in plan:
        grid[state.index[0]][state.index[1]] = 3

    grid[initial_state_index[0]][initial_state_index[1]] = -1
    grid[goal_state_index[0]][goal_state_index[1]] = 2

    plt.imshow(grid.T, origin="lower")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("grid2d.png")
