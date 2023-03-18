from planning.problems.grid3d_problem import build_problem, plot_results
from planning.search.backward import *
from planning.search.forward import *


if __name__ == '__main__':
    # Define search problem
    state_space, problem = build_problem()
    # Solve search problem
    solver = BreadthFirstForwardSearchAlgorithm(problem)
    success = solver.search()
    print(f"Success: {success}")
    # Get Plan
    plan = solver.get_plan()
    # Print / Plot results
    print("Plan:")
    for state in plan:
        print(state.index)
    plot_results(state_space, plan)
