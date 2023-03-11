from abc import ABCMeta
from enum import Enum
from typing import Any, List


class DiscreteStateStatus(Enum):
    UNVISITED = "UNVISITED"  # DiscreteState has not yet been visited
    DEAD = "DEAD"  # DiscreteState has been visited and for which every possibly next state has also been visited.
    ALIVE = "ALIVE"  # DiscreteState has been encountered, but possibly have unvisited next states.


class Action(metaclass=ABCMeta):
    pass


class DiscreteState:
    def __init__(self, index: Any, actions: List[Action], parent=None) -> None:
        self.index = index
        self.actions = actions
        self.parent = None
        self.status = DiscreteStateStatus.UNVISITED

    def __repr__(self) -> str:
        return f"index={self.index}. status={self.status}"

    def __eq__(self, other_state) -> bool:
        return self.index == other_state

    def mark_alive(self) -> None:
        self.status = DiscreteStateStatus.ALIVE

    def mark_dead(self) -> None:
        self.status = DiscreteStateStatus.DEAD

    def is_visited(self) -> bool:
        return self.status != DiscreteStateStatus.UNVISITED

    def get_actions(self) -> List[Action]:
        return self.actions

    def add_action(self, action: Action) -> None:
        self.actions.append(action)

    def set_parent(self, parent) -> None:
        self.parent = parent

    def get_parent(self) -> None:
        return self.parent


class DiscreteStateSpace:
    def __init__(self) -> None:
        self.space = {}

    def __repr__(self) -> str:
        s = ""
        for _, state in self.space.items():
            s += str(state) + "\n"
        return s

    def add_state(self, state: DiscreteState) -> None:
        self.space[state.index] = state

    def contains(self, state_to_check: DiscreteState) -> bool:
        for state in self.space:
            if state == state_to_check:
                return True
        return False
