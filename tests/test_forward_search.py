import unittest

from planning.search.algorithms import BreadthFirstForwardSearchAlgorithm
from planning.search.algorithms import DepthFirstForwardSearchAlgorithm
from planning.search.primitives import SearchResult
from planning.problems.grid2d_problem import build_problem

class TestForwardSearchAlgorithms(unittest.TestCase):
    def setUp(self) -> None:
        self.forward_search_impls = {"BreadthFirst": BreadthFirstForwardSearchAlgorithm,
                                    #  "DepthFirst": DepthFirstForwardSearchAlgorithm,
                                     }

    def test_solves_grid2d(self):
        _, problem = build_problem()
        self.assert_all_algorithms_solve_problem(problem)

    def assert_all_algorithms_solve_problem(self, problem):
        for name, algorithm in self.forward_search_impls.items():
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

    # def test_solves_grid3d(self):
    #     problem = 
    #     self.assert_all_algorithms_solve_problem(problem)


if __name__ == "__main__":
    unittest.main()
