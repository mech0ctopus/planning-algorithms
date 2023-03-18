from planning.problems.grid2d_problem import build_problem, plot_results
from planning.search.algorithms import BreadthFirstForwardSearchAlgorithm


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
