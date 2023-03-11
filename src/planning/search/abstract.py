from abc import ABCMeta, abstractmethod
from typing import List, Tuple
from planning.search.primitives import SearchResult
from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace


class StateTransitionFunction(metaclass=ABCMeta):
    @abstractmethod
    def get_next_state(self, current_state: DiscreteState, action: Action) -> DiscreteState:
        raise NotImplementedError


class SearchAlgorithm(metaclass=ABCMeta):
    """
    Abstract Discrete Feasible Planning `SearchAlgorithm`.

    Notation:
    X: self.state_space
    U: self.action_space
    f(x,u): self.transition_function
    x_I: self.initial_state
    X_G: self.goal_space
    x: self.current_state
    """
    def __init__(self, state_space: DiscreteStateSpace, transition_function: StateTransitionFunction,
                 initial_state: DiscreteState, goal_space: DiscreteStateSpace, verbose: bool) -> None:
        self.state_space = state_space
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.goal_space = goal_space
        self.verbose = verbose
        self.current_state = None
        self.plan = [] # list of state indices

    @abstractmethod
    def search(self) -> SearchResult:
        raise NotImplementedError

    def has_succeeded(self) -> bool:
        return self.goal_space.contains(self.current_state)

    def get_current_actions(self) -> List[Action]:
        return self.current_state.get_actions()

    def get_next_state(self, action: Action) -> DiscreteState:
        return self.transition_function.get_next_state(self.current_state, action, self.state_space)

    def get_plan(self) -> List[Tuple]:
        """
        Returns a list of state indices from initial_state to goal_state

        Assumes `search` has already been called.
        """
        plan = []
        planning_state = self.current_state

        while (parent := planning_state.get_parent()) is not None:
            plan.append(planning_state.index)
            planning_state = parent

        return list(reversed(plan))
