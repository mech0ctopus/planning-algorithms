from planning.search.abstract import PriorityQueue
from planning.search.abstract import SearchAlgorithm, StateTransitionFunction
from planning.search.primitives import SearchResult
from planning.space.primitives import DiscreteState, DiscreteStateSpace

from copy import deepcopy

# TODO: Add logic for checking if a state is `alive` or `dead` per p.33
# TODO: Raise exception if search fails (instead of Return code)

class ForwardSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.

    Q: self.priority_queue
    x': next_state
    """
    def __init__(self, state_space: DiscreteStateSpace,
                 transition_function: StateTransitionFunction, initial_state: DiscreteState,
                 goal_space: DiscreteStateSpace, priority_queue_type: PriorityQueue,
                 verbose: bool = False) -> None:
        super().__init__(state_space, transition_function, initial_state, goal_space, verbose)
        self.priority_queue = priority_queue_type()

    def search(self) -> SearchResult:
        self.priority_queue.add(self.initial_state)
        # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
        self.initial_state.mark_alive()

        while not self.priority_queue.is_empty():
            self.current_state = self.priority_queue.get()
            if self.verbose:
                print(f"Current State: {self.current_state}")

            if self.has_succeeded():
                return SearchResult.SUCCESS

            for action in self.get_current_actions():
                next_state = self.get_next_state(action)
                next_state.set_parent(deepcopy(self.current_state))
                # TODO: Store action taken from current_state -> next_state
                #       so that we can return it with our plan later on.
                if not next_state.is_visited():
                    # TODO: Algo states to "mark as visited", not "alive". Is this line correct?
                    next_state.mark_alive()
                    self.priority_queue.add(next_state)
                else:
                    continue

        return SearchResult.FAILURE
