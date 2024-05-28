from planning.search.abstract import UnidirectionalSearchAlgorithm
from planning.space.primitives import DiscreteState

from typing import List


class ForwardLabelCorrectingAlgorithm(UnidirectionalSearchAlgorithm):
    """
    Algorithm described in Figure 2.16 of Planning Algorithms by LaValle.

    A generalization of Dijkstra's algorithm, which upon termination produces an optimal plan (if one exists)
    for any prioritization of Q, as long as X is finite.
    """

    def search(self) -> None:
        # Line 1: Set state costs
        for state in self.problem.state_space:
            if state == self.problem.initial_state:
                state.set_cost(0)
            else:
                state.set_cost(float('inf'))
        # Line 2: Initialize queue
        self.priority_queue.add(self.problem.initial_state)
        # Line 3: Begin while loop
        while not self.priority_queue.is_empty():
            # Line 4: Select vertex
            self.current_state = self.priority_queue.get()
            # Line 5: For each possible action for the current state
            for action in self.get_current_actions():
                # Line 6: Propose a new state
                next_state = self.get_next_state(action)
                self.total_cost_to_come = self.current_state.get_cost() + action.cost
                # Line 7: Compare current cost with next state (Ignore Goal State Cost)
                if self.total_cost_to_come < next_state.get_cost():
                    # Insert a Directed Edge into the Graph
                    next_state.set_parent(self.current_state)
                    # Line 8: Update next state cost
                    next_state.set_cost(self.total_cost_to_come)
                    # Line 10: Insert next state into queue (Ignore Line 9)
                    self.priority_queue.add(next_state)

    def has_succeeded(self, goal_state: DiscreteState) -> bool:
        if goal_state not in self.problem.state_space:
            return False
        return goal_state.get_cost() != float('inf')

    def get_plan(self, goal_state: DiscreteState) -> List[DiscreteState]:
        if not self.has_succeeded(goal_state):
            return []  # Return an empty list if the goal state was not reached
        plan = []
        planning_state = goal_state
        while planning_state is not None:
            plan.append(planning_state)
            planning_state = planning_state.get_parent()
        return list(reversed(plan))  # Reverse to get the path from initial state to goal state

    def resolve_duplicate(self, state: DiscreteState) -> None:
        # Not needed here
        pass
