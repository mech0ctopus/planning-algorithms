import unittest
from unittest.mock import Mock

from planning.space.primitives import Action, DiscreteState, DiscreteStateSpace, DiscreteStateStatus


class TestDiscreteState(unittest.TestCase):
    def setUp(self):
        self.actions = [Mock(spec=Action) for _ in range(3)]
        self.state = DiscreteState(1, self.actions)

    def test_init(self):
        self.assertEqual(self.state.index, 1)
        self.assertEqual(self.state.actions, self.actions)
        self.assertIsNone(self.state.parent)
        self.assertEqual(self.state.status, DiscreteStateStatus.UNVISITED)

    def test_eq(self):
        self.assertEqual(self.state, 1)
        self.assertNotEqual(self.state, 2)

    def test_mark_alive(self):
        self.state.mark_alive()
        self.assertEqual(self.state.status, DiscreteStateStatus.ALIVE)

    def test_mark_dead(self):
        self.state.mark_dead()
        self.assertEqual(self.state.status, DiscreteStateStatus.DEAD)

    def test_is_visited(self):
        self.assertFalse(self.state.is_visited())
        self.state.mark_alive()
        self.assertTrue(self.state.is_visited())

    def test_get_actions(self):
        self.assertEqual(self.state.get_actions(), self.actions)

    def test_add_action(self):
        new_action = Mock(spec=Action)
        self.state.add_action(new_action)
        self.assertIn(new_action, self.state.actions)

    def test_set_parent(self):
        parent = Mock(spec=DiscreteState)
        self.state.set_parent(parent)
        self.assertEqual(self.state.parent, parent)

    def test_get_parent(self):
        parent = Mock(spec=DiscreteState)
        self.state.set_parent(parent)
        self.assertEqual(self.state.get_parent(), parent)


class TestDiscreteStateSpace(unittest.TestCase):
    def setUp(self):
        self.space = DiscreteStateSpace()
        self.state1 = DiscreteState(index=1, actions=[])
        self.state2 = DiscreteState(index=2, actions=[])

    def test_add_state(self):
        self.space.add_state(self.state1)
        self.assertIn(self.state1.index, self.space.space)
        self.assertEqual(self.space.space[self.state1.index], self.state1)

    def test_contains(self):
        self.space.add_state(self.state1)
        self.assertTrue(self.space.contains(self.state1))
        self.assertFalse(self.space.contains(self.state2))


if __name__ == "__main__":
    unittest.main()
