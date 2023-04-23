from planning.problems.five_state_problem import build_problem
from planning.search.backward import *
from planning.search.bidirectional import *
from planning.search.forward import *


if __name__ == '__main__':
    initial_state_index = 'a'
    goal_state_index = 'e'
    # Define search problem
    state_space, problem = build_problem(initial_state_index, goal_state_index)
    # Solve search problem
    solver = BreadthFirstBidirectionalSearchAlgorithm(problem)
    success = solver.search()
    print(f"Success: {success}")
    # Get Plan
    plan = solver.get_plan()
    # Print results
    solver.print_plan()
