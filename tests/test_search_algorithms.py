import unittest

from planning.search.algorithms import BreadthFirstForwardSearchAlgorithm
from planning.search.algorithms import DepthFirstForwardSearchAlgorithm
from planning.search.algorithms import BreadthFirstBackwardSearchAlgorithm
from planning.search.algorithms import DepthFirstBackwardSearchAlgorithm

from planning.problems import grid2d_problem, grid3d_problem


class SearchAlgorithmsTestBase(unittest.TestCase):
    def get_problems(self) -> None:
        return [
                grid2d_problem.build_problem(),
                grid3d_problem.build_problem(),
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
        self.assertTrue(success, f"{algorithm_name} solver failed!")

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

if __name__ == "__main__":
    unittest.main()
