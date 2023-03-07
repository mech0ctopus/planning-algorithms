from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Bool, List


class DiscreteStateStatus(Enum):
    UNVISITED = "UNVISITED"  # DiscreteState has not yet been visited
    DEAD = "DEAD"  # DiscreteState has been visited and for which every possibly next state has also been visited.
    ALIVE = "ALIVE"  # DiscreteState has been encountered, but possibly have unvisited next states.


# TODO: Need to assign some addition value to this State or something. Should this be abstract?
class DiscreteState:
    def __init__(self) -> None:
        self.status = DiscreteStateStatus.UNVISITED

    def mark_alive(self):
        self.status = DiscreteStateStatus.ALIVE

    def mark_dead(self):
        self.status = DiscreteStateStatus.DEAD

    def is_visited(self):
        return self.status != DiscreteStateStatus.UNVISITED


class DiscreteStateSpace:
    def __init__(self, states: List[DiscreteState]) -> None:
        self.space = states

    def contains(self, state: DiscreteState) -> Bool:
        #TODO: May need to do equality check instead of using "in"
        return state in self.space


class Action(metaclass=ABCMeta):
    pass


class ActionSpace(metaclass=ABCMeta):
    @abstractmethod
    def get_actions(self, state: DiscreteState) -> List[Action]:
        raise NotImplementedError
