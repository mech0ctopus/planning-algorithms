from search.abstract import SearchAlgorithm
from search.primitives import SearchResult, StateTransitionFunction
from space.primitives import ActionSpace, DiscreteState, DiscreteStateSpace

from collections import deque
from typing import Bool


class ForwardSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.

    Q: self.queue
    x': next_state
    """
    def __init__(self, state_space: DiscreteStateSpace, action_space: ActionSpace,
                 transition_function: StateTransitionFunction, initial_state: DiscreteState,
                 goal_space: DiscreteStateSpace) -> None:
        super().__init__(state_space, action_space, transition_function, initial_state, goal_space)
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
                # TODO: How can we access/index the proposed `next_state` in our global `state_space` context?
                    # Should the current_state, next_state, and transition_function all fall under the StateSpaceClass?
                next_state = self.get_next_state(action)
                if not next_state.is_visited():
                    # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
                    next_state.mark_alive()
                    self.queue.appendleft(next_state)
                else:
                    # TODO: Resolve duplicate `next_state`
                    raise NotImplementedError

        return SearchResult.FAILURE

    def queue_is_not_empty(self) -> Bool:
        return len(self.queue) > 0
