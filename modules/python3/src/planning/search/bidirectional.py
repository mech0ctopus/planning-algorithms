from planning.search.abstract import SearchAlgorithm, SearchProblem
from planning.search.backward import *
from planning.search.forward import *
from planning.space.primitives import DiscreteState, DiscreteStateStatus

from copy import deepcopy
from enum import Enum
from typing import List


class Direction(Enum):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    NONE = "NONE"

class BidirectionalSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.7 of Planning Algorithms by LaValle.
    """
    def __init__(self, problem: SearchProblem, forward_search_type: ForwardSearchAlgorithm,
                 backward_search_type: BackwardSearchAlgorithm) -> None:
        # Use deepcopy so that each search algorithm has an independent state-space
        # for marking states as "VISITED", etc.
        self.forward_search = forward_search_type(problem=deepcopy(problem))
        self.backward_search = backward_search_type(problem=deepcopy(problem))
        self.return_loop = Direction.NONE
        super().__init__(problem)

    def search(self) -> bool:
        #### 1. Initialization
        self.forward_search.priority_queue.add(self.forward_search.problem.initial_state)
        self.forward_search.problem.state_space.mark_visited(self.forward_search.problem.initial_state)

        for goal_state in self.backward_search.problem.goal_space:
            self.backward_search.priority_queue.add(goal_state)
            self.backward_search.problem.state_space.mark_visited(goal_state)

        while (not self.forward_search.priority_queue.is_empty()
               and not self.backward_search.priority_queue.is_empty()):

            if not self.forward_search.priority_queue.is_empty():
                #### 2. Select Vertex
                self.forward_search.current_state = self.forward_search.priority_queue.get()
                #### 5. Check for solution
                if self.backward_search.has_visited(self.forward_search.current_state):
                    self.intersection_state = self.forward_search.current_state
                    self.return_loop = Direction.FORWARD
                    print("Returning from Forward Loop")
                    return True
                #### 3. Apply an action
                for action in self.forward_search.get_current_actions():
                    next_forward_state = self.forward_search.get_next_state(action)

                    #### 4. Insert a Directed Edge into the Graph
                    if not self.forward_search.has_visited(next_forward_state):
                        next_forward_state.set_parent(self.forward_search.current_state)
                        self.problem.state_space.mark_visited(next_forward_state)
                        self.forward_search.problem.state_space.mark_visited(next_forward_state)
                        self.forward_search.priority_queue.add(next_forward_state)
                    else:
                        self.resolve_duplicate(next_forward_state)

            if not self.backward_search.priority_queue.is_empty():
                #### 2. Select Vertex
                next_backward_state = self.backward_search.priority_queue.get()
                #### 5. Check for solution
                if self.forward_search.has_visited(next_backward_state):
                    self.intersection_state = next_backward_state
                    print("Returning from Backward Loop")
                    self.return_loop = Direction.BACKWARD
                    return True
                #### 3. Apply an action
                for action in self.backward_search.get_previous_actions(next_backward_state):
                    self.backward_search.current_state = self.backward_search.get_previous_state(next_backward_state, action)

                    #### 4. Insert a Directed Edge into the Graph
                    if not self.backward_search.has_visited(self.backward_search.current_state):
                        self.backward_search.current_state.set_parent(next_backward_state)
                        self.problem.state_space.mark_visited(self.backward_search.current_state)
                        self.backward_search.problem.state_space.mark_visited(self.backward_search.current_state)
                        self.backward_search.priority_queue.add(self.backward_search.current_state)
                    else:
                        self.resolve_duplicate(self.backward_search.current_state)

        return False

    def get_plan(self) -> List[DiscreteState]:
        forward_plan, backward_plan = [], []

        print(f"Initial: {self.problem.initial_state}")
        print(f"Intersection: {self.intersection_state}")
        print(f"Goal: {self.problem.goal_space}")

        if self.return_loop == Direction.FORWARD:
            forward_plan = self.forward_search.get_plan()
        elif self.return_loop == Direction.BACKWARD:
            planning_state = self.forward_search.problem.state_space.get_state(self.intersection_state)
            while (parent := planning_state.get_parent()) is not None:
                forward_plan.append(planning_state)
                planning_state = parent
            forward_plan.append(self.problem.initial_state)
            forward_plan = list(reversed(forward_plan))
        else:
            raise Exception("Search failed (or was not called before `get_plan`).")

        return forward_plan + self.build_backward_plan_segment()

    def build_backward_plan_segment(self) -> List[DiscreteState]:
        backward_plan = []
        planning_state = self.backward_search.problem.state_space.get_state(self.intersection_state)
        while (parent := planning_state.get_parent()) not in self.problem.goal_space:
            backward_plan.append(planning_state)
            planning_state = parent
        backward_plan.append(planning_state)
        planning_state = parent
        backward_plan.append(planning_state)
        return backward_plan

class BreadthFirstBidirectionalSearchAlgorithm(BidirectionalSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        super().__init__(problem, forward_search_type=BreadthFirstForwardSearchAlgorithm,
                         backward_search_type=BreadthFirstBackwardSearchAlgorithm)

    def resolve_duplicate(self, current_state: DiscreteState) -> None:
        self.forward_search.resolve_duplicate(current_state)
        self.backward_search.resolve_duplicate(current_state)


class DepthFirstBidirectionalSearchAlgorithm(BidirectionalSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        super().__init__(problem, forward_search_type=DepthFirstForwardSearchAlgorithm,
                         backward_search_type=DepthFirstBackwardSearchAlgorithm)

    def resolve_duplicate(self, current_state: DiscreteState) -> None:
        self.forward_search.resolve_duplicate(current_state)
        self.backward_search.resolve_duplicate(current_state)
