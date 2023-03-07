from abc import ABCMeta, abstractmethod
from collections import deque
from enum import Enum
from typing import Bool, List
from spaces import Action, ActionSpace, DiscreteState, DiscreteStateSpace


class SearchResult(Enum):
    SUCCESS = True
    FAILURE = False


class StateTransitionFunction(metaclass=ABCMeta):
    @abstractmethod
    def get_next_state(self, current_state: DiscreteState, action: Action) -> DiscreteState:
        raise NotImplementedError


class SearchAlgorithm(metaclass=ABCMeta):
    """
    Abstract Discrete Feasible Planning `SearchAlgorithm`.

    Notation:
    x: self.current_state
    x_I: self.initial_state
    X_G: self.goal_space
    U: self.action_space
    f(x,u): self.transition_function
    """
    def __init__(self, initial_state: DiscreteState, goal_space: DiscreteStateSpace,
                 action_space: ActionSpace, transition_function: StateTransitionFunction) -> None:
        self.initial_state = initial_state
        self.goal_space = goal_space
        self.action_space = action_space
        self.transition_function = transition_function
        self.current_state = None

    @abstractmethod
    def search(self) -> SearchResult:
        raise NotImplementedError

    def has_succeeded(self) -> Bool:
        return self.goal_space.contains(self.current_state)

    def get_current_actions(self) -> List[Action]:
        return self.action_space.get_actions(self.current_state)

    def get_next_state(self, action: Action) -> DiscreteState:
        return self.transition_function.get_next_state(self.current_state, action)

# TODO: Need some sort of class-level container for StateSpace


class ForwardSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.

    Q: self.queue
    x': next_state
    """
    def __init__(self, initial_state: DiscreteState, goal_space: DiscreteStateSpace) -> None:
        super().__init__(initial_state, goal_space)
        self.queue = deque()

    def search(self) -> SearchResult:
        self.queue.appendleft(self.initial_state)
        # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
        self.initial_state.mark_alive()

        while self.queue_is_not_empty():
            self.current_state = self.queue.popleft()
            if self.has_succeeded():
                return SearchResult.SUCCESS

            for action in self.get_current_actions():
                next_state = self.get_next_state(action)
                if not next_state.is_visited():
                    # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
                    next_state.mark_alive()
                    self.queue.appendleft(next_state)
                else:
                    #TODO: Resolve duplicate `next_state`
                    raise NotImplementedError

        return SearchResult.FAILURE

    def queue_is_not_empty(self) -> Bool:
        return len(self.queue) > 0
