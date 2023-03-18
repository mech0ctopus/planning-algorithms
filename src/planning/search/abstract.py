from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List
from planning.search.primitives import SearchResult
from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace


class StateTransitionFunction(metaclass=ABCMeta):
    @abstractmethod
    def get_next_state(self, current_state: DiscreteState, action: Action) -> DiscreteState:
        raise NotImplementedError


class PriorityQueue(metaclass=ABCMeta):
    @abstractmethod
    def get(self) -> DiscreteState:
        """
        Get next state in the queue.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, state: DiscreteState) -> None:
        """
        Add a state to the Queue.
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        return len(self.queue) == 0


@dataclass
class SearchProblem(metaclass=ABCMeta):
    state_space: DiscreteStateSpace
    transition_function: StateTransitionFunction
    initial_state: DiscreteState
    goal_space: DiscreteStateSpace

    @abstractmethod
    def get_actions(self, state: DiscreteState) -> List[Action]:
        """
        U(x). Return all actions available for the current state.
        """
        raise NotImplementedError


class SearchAlgorithm(metaclass=ABCMeta):
    """
    Abstract Discrete Feasible Planning `SearchAlgorithm`.

    Notation:
    X: self.state_space
    U: self.action_space
    Q: self.priority_queue
    x': next_state
    f(x,u): self.transition_function
    x_I: self.initial_state
    X_G: self.goal_space
    x: self.current_state
    """
    def __init__(self, problem: SearchProblem, priority_queue_type: PriorityQueue, verbose: bool) -> None:
        self.problem = problem
        self.priority_queue = priority_queue_type()
        self.verbose = verbose
        self.current_state = None
        self.plan = [] # list of state indices

    @abstractmethod
    def search(self) -> SearchResult:
        raise NotImplementedError

    def has_succeeded(self) -> bool:
        return self.problem.goal_space.contains(self.current_state)

    def get_current_actions(self) -> List[Action]:
        return self.problem.get_actions(self.current_state)

    def get_next_state(self, action: Action) -> DiscreteState:
        return self.problem.transition_function.get_next_state(self.current_state, action, self.problem.state_space)

    def get_plan(self) -> List[DiscreteState]:
        """
        Returns a list of states from initial_state to goal_state

        Assumes `search` has already been called.
        """
        plan = []
        planning_state = self.current_state

        while (parent := planning_state.get_parent()) is not None:
            plan.append(planning_state)
            planning_state = parent

        # Append initial state
        plan.append(planning_state)

        return list(reversed(plan))

    @abstractmethod
    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        raise NotImplementedError
