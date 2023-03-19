from planning.search.abstract import SearchProblem, UnidirectionalSearchAlgorithm
from planning.search.queue import FIFO, LIFO
from planning.space.primitives import DiscreteState

from typing import List


class ForwardSearchAlgorithm(UnidirectionalSearchAlgorithm):
    """
    Algorithm described in Figure 2.4 of Planning Algorithms by LaValle.
    """
    def search(self) -> bool:
        #### 1. Initialization
        self.priority_queue.add(self.problem.initial_state)
        self.problem.initial_state.mark_visited()

        while not self.priority_queue.is_empty():
            #### 2. Select Vertex
            self.current_state = self.priority_queue.get()

            #### 5. Check for solution
            if self.has_succeeded():
                return True

            #### 3. Apply an action
            for action in self.get_current_actions():
                next_state = self.get_next_state(action)
                next_state.set_parent(self.current_state)
                # TODO: Store action taken from current_state -> next_state
                #       so that we can return it with our plan later on.
                # TODO: Calculate cost for taken this action.

                #### 4. Insert a Directed Edge into the Graph
                if not next_state.is_visited():
                    next_state.mark_visited()
                    self.priority_queue.add(next_state)
                else:
                    self.resolve_duplicate(next_state)

        return False

    def has_succeeded(self) -> bool:
        return self.problem.goal_space.contains(self.current_state)

    def get_plan(self) -> List[DiscreteState]:
        plan = []
        planning_state = self.current_state

        while (parent := planning_state.get_parent()) is not None:
            plan.append(planning_state)
            planning_state = parent

        # Append initial state
        plan.append(planning_state)

        return list(reversed(plan))


class BreadthFirstForwardSearchAlgorithm(ForwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        # Specify FIFO for all BreadthFirst
        priority_queue_type = FIFO
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        pass


class DepthFirstForwardSearchAlgorithm(ForwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        # Specify LIFO for all DepthFirst
        priority_queue_type = LIFO
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        pass


class DijkstrasForwardSearchAlgorithm(ForwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        raise NotImplementedError
        # TODO: Use a Fibonacci Heap
        priority_queue_type = None
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        # TODO: See bottom of P.36-37
        raise NotImplementedError


class AStarForwardSearchAlgorithm(ForwardSearchAlgorithm):
    # TODO: Possibly inherit from Dijkstra's. Just change the priority queue.
    def __init__(self, problem: SearchProblem) -> None:
        raise NotImplementedError
        priority_queue_type = None
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, next_state: DiscreteState) -> None:
        # TODO: See bottom of P.36-37
        raise NotImplementedError
