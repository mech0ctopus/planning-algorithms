import unittest

from planning.space.primitives import DiscreteState, DiscreteStateSpace, DiscreteStateStatus


class TestDiscreteState(unittest.TestCase):
    def setUp(self):
        self.state = DiscreteState(1)

    def test_init(self):
        self.assertEqual(self.state.index, 1)
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

    def test_set_parent(self):
        parent = DiscreteState(index=1)
        self.state.set_parent(parent)
        self.assertEqual(self.state.parent, parent)

    def test_get_parent(self):
        parent = DiscreteState(index=1)
        self.state.set_parent(parent)
        self.assertEqual(self.state.get_parent(), parent)


class TestDiscreteStateSpace(unittest.TestCase):
    def setUp(self):
        self.space = DiscreteStateSpace()
        self.state1 = DiscreteState(index=1)
        self.state2 = DiscreteState(index=2)
        self.state3 = DiscreteState(index=(2,3))

    def test_add_state(self):
        self.space.add_state(self.state1)
        self.assertIn(self.state1.index, self.space.space)
        self.assertEqual(self.space.space[self.state1.index], self.state1)

    def test_contains(self):
        self.space.add_state(self.state1)
        self.space.add_state(self.state3)
        self.assertTrue(self.space.contains(self.state1))
        self.assertFalse(self.space.contains(self.state2))
        self.assertTrue(self.space.contains(self.state3))


if __name__ == "__main__":
    unittest.main()
