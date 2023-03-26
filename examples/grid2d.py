from planning.problems.grid2d_problem import build_problem, plot_results
from planning.search.backward import *
from planning.search.bidirectional import *
from planning.search.forward import *


# INITIAL_STATE_IDX = (1,2)
# GOAL_STATE_IDX = (8,5)

if __name__ == '__main__':
    # Define search problem
    state_space, problem = build_problem()
    # Solve search problem
    # solver = BreadthFirstBackwardSearchAlgorithm(problem)
    solver = BreadthFirstBidirectionalSearchAlgorithm(problem)
    success = solver.search()
    print(f"Success: {success}")
    # Get Plan
    plan = solver.get_plan()
    # Print / Plot results
    print("Plan:")
    for state in plan:
        print(state.index)
    plot_results(state_space, plan)
