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
    def __init__(self, index: Any, actions: List[Action]) -> None:
        self.index = index
        self.actions = actions
        self.status = DiscreteStateStatus.UNVISITED

    def mark_alive(self) -> None:
        self.status = DiscreteStateStatus.ALIVE

    def mark_dead(self) -> None:
        self.status = DiscreteStateStatus.DEAD

    def is_visited(self) -> bool:
        return self.status != DiscreteStateStatus.UNVISITED

    def get_actions(self) -> List[Action]:
        return self.actions


class DiscreteStateSpace:
    def __init__(self) -> None:
        self.space = {}

    def add_state(self, state: DiscreteState) -> None:
        self.space[state.index] = state

    def contains(self, state_to_check: DiscreteState) -> bool:
        #TODO: Can we use `state_to_check in self.space` here?
        for state in self.space:
            if state == state_to_check:
                return True
        return False
