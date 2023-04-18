from planning.problems.grid3d_problem import build_problem, plot_results
from planning.search.backward import *
from planning.search.bidirectional import *
from planning.search.forward import *


if __name__ == '__main__':
    initial_state_index = (1,2,3)
    goal_state_index = (12,13,10)  
    # Define search problem
    state_space, problem = build_problem(initial_state_index, goal_state_index)
    # Solve search problem
    solver = BreadthFirstBidirectionalSearchAlgorithm(problem)
    success = solver.search()
    print(f"Success: {success}")
    # Get Plan
    plan = solver.get_plan()
    # Print / Plot results
    solver.print_plan()
    plot_results(state_space, plan, initial_state_index, goal_state_index)
