from planning.search.abstract import SearchProblem, UnidirectionalSearchAlgorithm
from planning.search.queue import FIFO, LIFO
from planning.space.primitives import DiscreteState

from typing import List


class BackwardSearchAlgorithm(UnidirectionalSearchAlgorithm):
    """
    Algorithm described in Figure 2.6 of Planning Algorithms by LaValle.
    """
    def search(self) -> bool:
        #### 1. Initialization
        for goal_state in self.problem.goal_space:
            self.priority_queue.add(goal_state)
            goal_state.mark_visited()

        while not self.priority_queue.is_empty():
            #### 2. Select Vertex
            next_state = self.priority_queue.get()

            #### 5. Check for solution
            if self.has_succeeded():
                return True

            #### 3. Apply an action
            for action in self.get_previous_actions(next_state):
                self.current_state = self.get_previous_state(next_state, action)
                self.current_state.set_parent(next_state)
 
                #### 4. Insert a Directed Edge into the Graph
                if not self.current_state.is_visited():
                    self.current_state.mark_visited()
                    self.priority_queue.add(self.current_state)
                else:
                    self.resolve_duplicate(self.current_state)

                #### 5. Check for solution (added to resolve five-state problem failure)
                if self.has_succeeded():
                    return True

        return False

    def has_succeeded(self) -> bool:
        return self.current_state == self.problem.initial_state

    def get_plan(self) -> List[DiscreteState]:
        plan = []
        planning_state = self.current_state

        while (parent := planning_state.get_parent()) not in self.problem.goal_space:
            plan.append(planning_state)
            planning_state = parent

        plan.append(planning_state)
        plan.append(parent)

        return plan


class BreadthFirstBackwardSearchAlgorithm(BackwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        # Specify FIFO for all BreadthFirst
        priority_queue_type = FIFO
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, current_state: DiscreteState) -> None:
        pass


class DepthFirstBackwardSearchAlgorithm(BackwardSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        # Specify LIFO for all DepthFirst
        priority_queue_type = LIFO
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, current_state: DiscreteState) -> None:
        pass
