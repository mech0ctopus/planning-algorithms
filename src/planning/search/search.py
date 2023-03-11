from planning.search.abstract import SearchAlgorithm, StateTransitionFunction
from planning.search.primitives import SearchResult
from planning.space.primitives import DiscreteState, DiscreteStateSpace

from collections import deque

# TODO: Add logic for checking if a state is `alive` or `dead` per p.33


class ForwardSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.

    Q: self.queue
    x': next_state
    """
    def __init__(self, state_space: DiscreteStateSpace,
                 transition_function: StateTransitionFunction, initial_state: DiscreteState,
                 goal_space: DiscreteStateSpace, verbose: bool = True) -> None:
        super().__init__(state_space, transition_function, initial_state, goal_space, verbose)
        self.queue = deque()

    def search(self) -> SearchResult:
        self.queue.appendleft(self.initial_state)
        # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
        self.initial_state.mark_alive()

        while self.queue_is_not_empty():
            self.current_state = self.queue.popleft()
            if self.verbose:
                print(f"Current State: {self.current_state}")

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
                    continue

        return SearchResult.FAILURE

    def queue_is_not_empty(self) -> bool:
        return len(self.queue) > 0
