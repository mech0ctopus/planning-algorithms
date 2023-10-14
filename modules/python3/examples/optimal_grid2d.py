from planning.space.primitives import DiscreteState
from planning.problems.grid2d_problem import build_problem, plot_results
from planning.search.optimal import ForwardLabelCorrectingAlgorithm
from planning.search.queue import FIFO

if __name__ == '__main__':
    initial_state_index = (6, 2)
    goal_state_index = (12, 12)
    # Define search problem
    state_space, problem = build_problem(initial_state_index, goal_state_index)
    goal_state = state_space.get_state(DiscreteState(index=goal_state_index))
    # Solve search problem
    solver = ForwardLabelCorrectingAlgorithm(problem, priority_queue_type=FIFO)
    success = solver.search(goal_state)
    print(f"Success: {success}")
    # Get Plan
    plan = solver.get_plan(goal_state=goal_state)
    # Print / Plot results
    solver.print_plan(goal_state=goal_state)
    plot_results(problem, plan, initial_state_index, goal_state_index)
