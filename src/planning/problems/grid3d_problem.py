# A robot moving on a 3d grid

from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace
from planning.search.abstract import SearchProblem, StateTransitionFunction
from planning.search.algorithms import BreadthFirstForwardSearchAlgorithm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D  # noqa
import numpy as np
from typing import List

# TODO: Resolve zero-index / one-index issue. Plot is off by 1 spot in X and Y
# TODO: Cleanup / Refactor this example.

XMAX = 15
YMAX = 15
ZMAX = 15
INITIAL_STATE_IDX = (1,2,3)
GOAL_STATE_IDX = (8,5,10)


class MoveOn3dGrid(Action):
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z


class GridStateTransitionFunction(StateTransitionFunction):
    def get_next_state(self, current_state: DiscreteState, action: MoveOn3dGrid,
                       state_space: DiscreteStateSpace) -> DiscreteState:      
        next_state_idx = (current_state.index[0] + action.x,
                          current_state.index[1] + action.y,
                          current_state.index[2] + action.z)
        return state_space.space[next_state_idx]


class Grid3dSearchProblem(SearchProblem):
    def get_actions(self, state: DiscreteState) -> List[Action]:
        x, y, z = state.index
        # Non-Border cells
        if 0 < x < (XMAX - 1) and 0 < y < (YMAX - 1) and  0 < z < (ZMAX - 1):
            actions = [MoveOn3dGrid(-1, 0, 0),
                       MoveOn3dGrid(1, 0, 0),
                       MoveOn3dGrid(0, -1, 0),
                       MoveOn3dGrid(0, 1, 0),
                       MoveOn3dGrid(0, 0, -1),
                       MoveOn3dGrid(0, 0, 1),
                       ]
        else:
            actions = []
            if x == 0:
                actions.append(MoveOn3dGrid(1, 0, 0))
            if y == 0:
                actions.append(MoveOn3dGrid(0, 1, 0))
            if z == 0:
                actions.append(MoveOn3dGrid(0, 0, 1))
            if x == XMAX:
                actions.append(MoveOn3dGrid(-1, 0, 0))
            if y == YMAX:
                actions.append(MoveOn3dGrid(0, -1, 0))
            if z == ZMAX:
                actions.append(MoveOn3dGrid(0, 0, -1))
        return actions

def build_state_space():
    state_space = DiscreteStateSpace()
    for x in range(XMAX):
        for y in range (YMAX):
            for z in range (ZMAX):
                state = DiscreteState(index=(x,y,z))
                state_space.add_state(state)  
    return state_space


def build_goal_space():
    goal_space = DiscreteStateSpace()
    goal_state = DiscreteState(index=GOAL_STATE_IDX)
    goal_space.add_state(goal_state)
    return goal_space


def plot_results(state_space, plan):
    grid = np.zeros((XMAX, YMAX, ZMAX))
    colors = np.zeros((XMAX, YMAX, ZMAX, 4), dtype=np.float32)

    alpha = .5
    visited_color = [0, 0, 0, 0.2]
    plan_color = [0, 1, 0, 1]
    initial_color = [0, 0, 1, alpha]
    goal_color = [1, 1, 0, alpha]

    # VISITED
    # for x in range(XMAX):
    #     for y in range(YMAX):
    #         for z in range(ZMAX):
    #             grid[x, y, z] = state_space.space[(x,y,z)].is_visited()
    #             if grid[x, y, z]:
    #                 colors[x, y, z] = visited_color

    # PLAN
    for state in plan:
        grid[state.index[0]][state.index[1]][state.index[2]] = 3
        colors[state.index[0]][state.index[1]][state.index[2]] = plan_color

    # INITIAL
    grid[INITIAL_STATE_IDX[0]][INITIAL_STATE_IDX[1]][INITIAL_STATE_IDX[2]] = -1
    colors[INITIAL_STATE_IDX[0]][INITIAL_STATE_IDX[1]][INITIAL_STATE_IDX[2]] = initial_color
    # GOAL
    grid[GOAL_STATE_IDX[0]][GOAL_STATE_IDX[1]][GOAL_STATE_IDX[2]] = 2
    colors[GOAL_STATE_IDX[0]][GOAL_STATE_IDX[1]][GOAL_STATE_IDX[2]] = goal_color

    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(grid, facecolors=colors, edgecolor='k')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("grid3d.png")

def build_problem():
    state_space = build_state_space()
    problem = Grid3dSearchProblem(state_space=state_space,
                                  goal_space=build_goal_space(),
                                  transition_function=GridStateTransitionFunction(),
                                  initial_state = state_space.space[INITIAL_STATE_IDX]
                                  )
    return state_space, problem