from planning.search.abstract import PriorityQueue, SearchAlgorithm, SearchProblem
from planning.search.queue import FIFO, LIFO
from planning.space.primitives import DiscreteState, DiscreteStateSpace

from typing import List


class BidirectionalSearchAlgorithm(SearchAlgorithm):
    """
    Algorithm described in Figure 2.7 of Planning Algorithms by LaValle.

    Notation:
        Q_I: self.priority_queue_initial
        Q_G: self.priority_queue_goal
    """
    def __init__(self, problem: SearchProblem, priority_queue_type: PriorityQueue) -> None:
        self.priority_queue_initial = priority_queue_type()
        self.priority_queue_goal = priority_queue_type()
        self.visited_states_initial = DiscreteStateSpace()
        self.visited_states_goal = DiscreteStateSpace()
        super().__init__(problem)

    def search(self) -> bool:
        #### 1. Initialization
        self.intersection_state = None
        self.priority_queue_initial.add(self.problem.initial_state)
        self.problem.initial_state.mark_visited()
        self.visited_states_initial.add_state(self.problem.initial_state)

        for goal_state in self.problem.goal_space:
            self.priority_queue_goal.add(goal_state)
            goal_state.mark_visited()
            self.visited_states_goal.add_state(goal_state)

        while (not self.priority_queue_initial.is_empty()
               and not self.priority_queue_goal.is_empty()):

            if not self.priority_queue_initial.is_empty():
                #### 2. Select Vertex
                self.current_state = self.priority_queue_initial.get()
                #### 5. Check for solution
                if self.visited_from_goal_search(self.current_state):
                    self.intersection_state = self.current_state
                    return True
                #### 3. Apply an action
                for action in self.get_current_actions():
                    next_state = self.get_next_state(action)
                    next_state.set_parent(self.current_state)
                    #### 4. Insert a Directed Edge into the Graph
                    if not self.visited_from_initial_search(next_state):
                        next_state.mark_visited()
                        self.visited_states_initial.add_state(next_state)
                        self.priority_queue_initial.add(next_state)
                    else:
                        self.resolve_duplicate(next_state)

            if not self.priority_queue_goal.is_empty():
                #### 2. Select Vertex
                next_state = self.priority_queue_goal.get()
                #### 5. Check for solution
                if self.visited_from_initial_search(next_state):
                    self.intersection_state = next_state
                    return True
                #### 3. Apply an action
                for action in self.get_previous_actions(next_state):
                    self.current_state = self.get_previous_state(next_state, action)
                    self.current_state.set_parent(next_state)

                    #### 4. Insert a Directed Edge into the Graph
                    if not self.visited_from_goal_search(self.current_state):
                        self.current_state.mark_visited()
                        self.visited_states_goal.add_state(self.current_state)
                        self.priority_queue_goal.add(self.current_state)
                    else:
                        self.resolve_duplicate(self.current_state)

        return False

    def visited_from_goal_search(self, state: DiscreteState) -> bool:
        return self.visited_states_goal.contains(state)

    def visited_from_initial_search(self, state: DiscreteState) -> bool:
        return self.visited_states_initial.contains(state)

    def get_plan(self) -> List[DiscreteState]:
        plan = []

        print("Initial Branch plan from initial to intersection")
        planning_state = self.problem.initial_state
        while (parent := planning_state.get_parent()) is not None \
              and (parent != self.intersection_state):
            plan.append(planning_state)
            planning_state = parent

        print("Goal Branch plan from intersection to goal")
        planning_state = self.intersection_state
        while (parent := planning_state.get_parent()) not in self.problem.goal_space:
            plan.append(planning_state)
            planning_state = parent
        plan.append(planning_state)
        plan.append(parent)

        return plan


class BreadthFirstBidirectionalSearchAlgorithm(BidirectionalSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        # Specify FIFO for all BreadthFirst
        priority_queue_type = FIFO
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, current_state: DiscreteState) -> None:
        pass


class DepthFirstBidirectionalSearchAlgorithm(BidirectionalSearchAlgorithm):
    def __init__(self, problem: SearchProblem) -> None:
        # Specify LIFO for all DepthFirst
        priority_queue_type = LIFO
        super().__init__(problem, priority_queue_type)

    def resolve_duplicate(self, current_state: DiscreteState) -> None:
        pass
