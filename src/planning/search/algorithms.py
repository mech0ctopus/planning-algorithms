from planning.search.abstract import PriorityQueue
from planning.search.abstract import SearchAlgorithm, SearchProblem
from planning.search.primitives import SearchResult
from planning.search.queue import FIFO, LIFO
from planning.space.primitives import DiscreteState

from abc import abstractmethod


class ForwardSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.

    Q: self.priority_queue
    x': next_state
    """
    def __init__(self, problem: SearchProblem, priority_queue_type: PriorityQueue,
                 verbose: bool = False) -> None:
        super().__init__(problem, verbose)
        self.priority_queue = priority_queue_type()

    def search(self) -> SearchResult:
        self.priority_queue.add(self.problem.initial_state)
        self.problem.initial_state.mark_visited()

        while not self.priority_queue.is_empty():
            self.current_state = self.priority_queue.get()
            if self.verbose:
                print(f"Current State: {self.current_state}")

            if self.has_succeeded():
                return SearchResult.SUCCESS

            for action in self.get_current_actions():
                next_state = self.get_next_state(action)
                next_state.set_parent(self.current_state)
                # TODO: Store action taken from current_state -> next_state
                #       so that we can return it with our plan later on.
                # TODO: Calculate cost for taken this action.
                if not next_state.is_visited():
                    next_state.mark_visited
                    self.priority_queue.add(next_state)
                else:
                    self.resolve_duplicate(next_state)

        return SearchResult.FAILURE

    @abstractmethod
    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        raise NotImplementedError


class BreadthFirstForwardSearchAlgorithm(ForwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem, verbose: bool = False) -> None:
        # Specify FIFO for all BreadthFirst
        priority_queue_type = FIFO
        super().__init__(problem, priority_queue_type, verbose)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        pass


class DepthFirstForwardSearchAlgorithm(ForwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem, verbose: bool = False) -> None:
        # Specify LIFO for all DepthFirst
        priority_queue_type = LIFO
        super().__init__(problem, priority_queue_type, verbose)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        pass


class DijkstrasForwardSearchAlgorithm(ForwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem, verbose: bool = False) -> None:
        raise NotImplementedError
        # TODO: Use a Fibonacci Heap
        priority_queue_type = None
        super().__init__(problem, priority_queue_type, verbose)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        # TODO: See bottom of P.36-37
        raise NotImplementedError


class AStarForwardSearchAlgorithm(ForwardSearchAlgorithm):
    # TODO: Possibly inherit from Dijkstra's. Just change the priority queue.
    def __init__(self, problem: SearchProblem, verbose: bool = False) -> None:
        raise NotImplementedError
        priority_queue_type = None
        super().__init__(problem, priority_queue_type, verbose)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        # TODO: See bottom of P.36-37
        raise NotImplementedError
