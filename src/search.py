from abc import ABCMeta, abstractmethod
from collections import deque
from enum import Enum
from typing import Bool, List


class DiscreteStateStatus(Enum):
    UNVISITED = "UNVISITED"  # DiscreteState has not yet been visited
    DEAD = "DEAD"  # DiscreteState has been visited and for which every possibly next state has also been visited.
    ALIVE = "ALIVE"  # DiscreteState has been encountered, but possibly have unvisited next states.

class SearchResult(Enum):
    SUCCESS = True
    FAILURE = False

class DiscreteState:
    def __init__(self) -> None:
        self.status = DiscreteStateStatus.UNVISITED

    def mark_alive(self):
        self.status = DiscreteStateStatus.ALIVE

    def mark_dead(self):
        self.status = DiscreteStateStatus.DEAD


class DiscreteStateSpace:
    def __init__(self, states: List[DiscreteState]) -> None:
        self.space = states

    def contains(self, state: DiscreteState) -> Bool:
        #TODO: May need to do equality check instead of using "in"
        return state in self.space


class SearchAlgorithm(metaclass=ABCMeta):
    """

    # Notation
    x: self.current_state
    x_I: self.initial_state
    X_G: self.goal_space
    """
    def __init__(self, initial_state: DiscreteState, goal_space: DiscreteStateSpace) -> None:
        self.initial_state = initial_state
        self.goal_space = goal_space
        self.current_state = None

    @abstractmethod
    def search(self) -> SearchResult:
        raise NotImplementedError

    def has_succeeded(self) -> Bool:
        return self.goal_space.contains(self.current_state)

class ForwardSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.

    Q: self.queue
    """
    def __init__(self, initial_state: DiscreteState, goal_space: DiscreteStateSpace) -> None:
        super().__init__(initial_state, goal_space)
        self.queue = deque()

    def search(self) -> SearchResult:
        self.queue.appendleft(self.initial_state)
        # TODO: Algo states "mark as visited", not "alive". Is this correct?
        self.initial_state.mark_alive()

        while self.queue_is_not_empty():
            self.current_state = self.queue.popleft()
            if self.has_succeeded():
                return SearchResult.SUCCESS
            #TODO: Resume work here (Line 6 in algorithm)


        return ...

    def queue_is_not_empty(self) -> Bool:
        return len(self.queue) > 0