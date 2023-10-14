from abc import ABCMeta
from enum import Enum
from typing import Any


class DiscreteStateStatus(Enum):
    UNVISITED = "UNVISITED"  # DiscreteState has not yet been visited
    DEAD = "DEAD"  # DiscreteState has been visited and for which every possibly next state has also been visited.
    ALIVE = "ALIVE"  # DiscreteState has been encountered, but possibly have unvisited next states.


class Action(metaclass=ABCMeta):
    pass


class DiscreteState:
    def __init__(self, index: Any, parent=None, status=DiscreteStateStatus.UNVISITED) -> None:
        self.index = index
        self.parent = parent
        self.status = status
        self.cost = 0

    def __repr__(self) -> str:
        if self.parent is not None:
            parent_s = f" <- parent_id: {self.parent.index}"
        else:
            parent_s = ""
        return f"index={self.index}. cost={self.cost}. status={self.status}" + parent_s

    def __eq__(self, other_state) -> bool:
        return self.index == other_state

    def mark_alive(self) -> None:
        self.status = DiscreteStateStatus.ALIVE

    def mark_dead(self) -> None:
        self.status = DiscreteStateStatus.DEAD

    def mark_visited(self) -> None:
        # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
        self.mark_alive()

    def is_visited(self) -> bool:
        return self.status != DiscreteStateStatus.UNVISITED

    def set_parent(self, parent, raise_exception=False) -> None:
        if raise_exception and self.parent is not None:
            raise ValueError(f"Parent is being overwritten! {self}")
        self.parent = DiscreteState.copy(parent)

    def get_parent(self) -> None:
        return self.parent

    def set_cost(self, new_cost: float) -> None:
        self.cost = new_cost

    def get_cost(self) -> float:
        return self.cost

    @staticmethod
    def copy(state):
        """
        Construct a new state object to avoid `RecursionError`s related to deepcopy.
        This method is also substantially faster than creating `deepcopy`s.
        """
        return DiscreteState(index=state.index, parent=state.parent, status=state.status)


class DiscreteStateSpace:
    def __init__(self) -> None:
        self.space = {}

    def __repr__(self) -> str:
        s = ""
        for _, state in self.space.items():
            s += str(state) + "\n"
        return s

    def __iter__(self):
        for state in self.space.values():
            yield state

    def add_state(self, state: DiscreteState) -> None:
        self.space[state.index] = state

    def contains(self, state_to_check: DiscreteState) -> bool:
        return state_to_check.index in self.space.keys()

    def has_visited(self, state: DiscreteState) -> bool:
        return self.get_state(state).is_visited()

    def get_state(self, state: DiscreteState) -> DiscreteState:
        return self.space[state.index]

    def mark_visited(self, state: DiscreteState) -> None:
        self.get_state(state).mark_visited()
