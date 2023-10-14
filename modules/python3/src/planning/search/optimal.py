from planning.search.abstract import UnidirectionalSearchAlgorithm
from planning.space.primitives import DiscreteState

from typing import List


class ForwardLabelCorrectingAlgorithm(UnidirectionalSearchAlgorithm):
    """
    Algorithm described in Figure 2.16 of Planning Algorithms by LaValle.

    A generalization of Dijkstra's algorithm, which upon termination produces an optimal plan (if one exists)
    for any prioritization of Q, as long as X is finite.
    """

    def search(self, goal_state: DiscreteState) -> bool:
        # Goal State is passed in for convenience. This assumes a single goal state
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
                # Line 7: Compare current cost with next state, goal state
                if self.total_cost_to_come < min(next_state.get_cost(), goal_state.get_cost()):
                    # Insert a Directed Edge into the Graph
                    next_state.set_parent(self.current_state)
                    # Line 8: Update next state cost
                    next_state.set_cost(self.total_cost_to_come)
                    # Line 9: If next state is not goal state
                    if next_state != goal_state:
                        # Line 10: Insert next state into queue
                        self.priority_queue.add(next_state)

        return self.has_succeeded(goal_state)

    def has_succeeded(self, goal_state: DiscreteState) -> bool:
        return goal_state.get_cost() != float('inf')

    def get_plan(self, goal_state: DiscreteState) -> List[DiscreteState]:
        plan = []
        planning_state = goal_state

        while (parent := planning_state.get_parent()) is not None:
            plan.append(planning_state)
            planning_state = parent

        # Append initial state
        if plan[-1] != self.problem.goal_space:
            plan.append(planning_state)

        return list(reversed(plan))

    def resolve_duplicate(self, state: DiscreteState) -> None:
        # Not needed here
        pass
