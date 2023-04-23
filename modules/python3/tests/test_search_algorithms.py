import unittest

from planning.search.backward import *
from planning.search.bidirectional import *
from planning.search.forward import *

from planning.problems import five_state_problem, grid2d_problem, grid3d_problem


class SearchAlgorithmsTestBase(unittest.TestCase):
    def get_problems(self) -> None:
        return [
                # 2D Grid
                grid2d_problem.build_problem(initial_state_index=(6,3), goal_state_index=(3,9)),
                grid2d_problem.build_problem(initial_state_index=(1,10), goal_state_index=(8,1)),
                grid2d_problem.build_problem(initial_state_index=(3,8), goal_state_index=(12,2)),
                grid2d_problem.build_problem(initial_state_index=(10,2), goal_state_index=(5,5)),
                grid2d_problem.build_problem(initial_state_index=(12,4), goal_state_index=(2,7)), 
                # 3D Grid
                grid3d_problem.build_problem(initial_state_index=(3,11,8), goal_state_index=(6,2,6)),
                grid3d_problem.build_problem(initial_state_index=(5,8,12), goal_state_index=(12,13,10)),
                grid3d_problem.build_problem(initial_state_index=(3,5,1), goal_state_index=(3,7,5)),
                grid3d_problem.build_problem(initial_state_index=(4,5,10), goal_state_index=(2,2,10)),
                grid3d_problem.build_problem(initial_state_index=(10,2,8), goal_state_index=(2,8,12)),
                # Five State
                five_state_problem.build_problem(initial_state_index='a', goal_state_index='e'),
                five_state_problem.build_problem(initial_state_index='a', goal_state_index='d'),
                five_state_problem.build_problem(initial_state_index='b', goal_state_index='a'),
                five_state_problem.build_problem(initial_state_index='d', goal_state_index='a'),
                five_state_problem.build_problem(initial_state_index='d', goal_state_index='b'),
                ]

    def assert_all_algorithms_solve_all_problems(self):
        for name, algorithm in self.algorithms.items():
          self.assert_algorithm_solves_all_problems(name=name, algorithm=algorithm)  

    def assert_algorithm_solves_all_problems(self, name, algorithm):
        for _, problem in self.get_problems():
            self.assert_algorithm_solves_problem(name, algorithm, problem)

    def assert_algorithm_solves_problem(self, algorithm_name, algorithm, problem):
        solver = algorithm(problem)
        success = solver.search()
        self.assertTrue(success, f"\n{algorithm_name} solver of type {type(solver)} failed for "
                                 f"problem type {type(problem)} with\n"
                                 f"Initial: {problem.initial_state}\n"
                                 f"Goal: {problem.goal_space}.")

        plan = solver.get_plan()
        self.assert_plan_connects_initial_and_goal_states(plan, algorithm_name, problem)

    def assert_plan_connects_initial_and_goal_states(self, plan, algorithm_name, problem):
        self.assertEqual(problem.initial_state, plan[0],
                         f"Plan from {algorithm_name} does not start at the initial state!")
        self.assertTrue(problem.goal_space.contains(plan[-1]),
                        f"Plan from {algorithm_name} does not end in the goal space!")


class TestForwardSearchAlgorithms(SearchAlgorithmsTestBase):
    def setUp(self) -> None:
        self.algorithms = {
                           "BreadthFirst": BreadthFirstForwardSearchAlgorithm,
                           "DepthFirst": DepthFirstForwardSearchAlgorithm,
                           }

    def test_forward_search(self):
        self.assert_all_algorithms_solve_all_problems()


class TestBackwardSearchAlgorithms(SearchAlgorithmsTestBase):
    def setUp(self) -> None:
        self.algorithms = {
                           "BreadthFirst": BreadthFirstBackwardSearchAlgorithm,
                           "DepthFirst": DepthFirstBackwardSearchAlgorithm,
                           }

    def test_backward_search(self):
        self.assert_all_algorithms_solve_all_problems()


class TestBidirectionalSearchAlgorithms(SearchAlgorithmsTestBase):
    def setUp(self) -> None:
        self.algorithms = {
                           "BreadthFirst": BreadthFirstBidirectionalSearchAlgorithm,
                           "DepthFirst": DepthFirstBidirectionalSearchAlgorithm,
                           }

    def test_bidirectional_search(self):
        self.assert_all_algorithms_solve_all_problems()


if __name__ == "__main__":
    unittest.main()
