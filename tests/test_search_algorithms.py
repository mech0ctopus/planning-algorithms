import unittest

from planning.search.algorithms import BreadthFirstForwardSearchAlgorithm
from planning.search.algorithms import DepthFirstForwardSearchAlgorithm
from planning.search.primitives import SearchResult
from planning.problems import grid2d_problem, grid3d_problem


class TestSearchAlgorithms(unittest.TestCase):
    def setUp(self) -> None:
        self.problems = [grid2d_problem.build_problem(),
                         grid3d_problem.build_problem()]

    def assert_algorithm_solves_all_problems(self, name, algorithm):
        for _, problem in self.problems:
            self.assert_algorithm_solves_problem(name, algorithm, problem)

    def assert_algorithm_solves_problem(self, algorithm_name, algorithm, problem):
        solver = algorithm(problem)
        success = solver.search()
        self.assertEqual(success, SearchResult.SUCCESS,
                         f"{algorithm_name} solver failed!")

        plan = solver.get_plan()
        self.assert_plan_connects_initial_and_goal_states(plan, algorithm_name, problem)

    def assert_plan_connects_initial_and_goal_states(self, plan, algorithm_name, problem):
        self.assertEqual(problem.initial_state, plan[0],
                         f"Plan from {algorithm_name} does not start at the initial state!")
        self.assertTrue(problem.goal_space.contains(plan[-1]),
                        f"Plan from {algorithm_name} does not end in the goal space!")


class TestForwardSearchAlgorithms(TestSearchAlgorithms):
    def test_breadthfirst_solves_all_problems(self):
        self.assert_algorithm_solves_all_problems(name="BreadthFirst",
                                                  algorithm=BreadthFirstForwardSearchAlgorithm)

    def test_depthfirst_solves_all_problems(self):
        self.assert_algorithm_solves_all_problems(name="DepthFirst",
                                                  algorithm=DepthFirstForwardSearchAlgorithm)


if __name__ == "__main__":
    unittest.main()
