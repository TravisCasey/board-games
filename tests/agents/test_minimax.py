import unittest
from context import game, IDDFSAgent, MaxnAgent, ParanoidAgent


class TestIDDFSAgent(unittest.TestCase):

    def setUp(self):
        self.agent_1 = IDDFSAgent(prune_enable=False,
                                  verbose=5)
        self.agent_2 = IDDFSAgent(name='Pruning DFS Agent',
                                  verbose=5)
        self.tree_1 = game.Tree(
            [(1.0, 1.0, 1.0),
             [(1.0, 4.0, 4.0),
              [(2.0, 3.0, 0.0)],
              [(1.0, 1.0, 0.0)]],
             [(0.0, 1.0, 2.0),
              [(4.0, 0.0, 4.0)],
              [(1.0, 1.0, 1.0)]]],
            3,
            4.0,
            0.0,
            9.0)
        self.tree_2 = game.Tree(
            [(7.0, -3.5, 6.0, 0.9),
             [(1.0, 7.0, 2.2, -5.0),
              [(1.0, 5.0, -9.5, 3.0),
               [(2.0, -8.0, 1.0, 2.0)],
               [(1.0, -7.2, 2.0, 4.0)],
               [(-2.0, 0.4, 4.0, 5.0)]],
              [(-2.3, 2.0, -2.0, 3.0)]],
             [(2.1, 2.0, -1.1, 0.5)]],
            4,
            7.0,
            -9.5,
            10.4)
        self.tree_3 = game.Tree(
            [(3.0, -3.0),
             [(2.4, -2.4),
              [(5.0, -5.0),
               [(-10.0, 10.0)],
               [(-8.0, 8.0)],
               [(4.0, -4.0)]],
              [(-8.0, 8.0),
               [(3.0, -3.0)],
               [(5.0, -5.0)],
               [(-2.0, 2.0)]],
              [(-5.0, 5.0)]],
             [(-3.0, 3.0),
              [(0.0, 0.0)],
              [(1.0, -1.0)],
              [(4.0, -4.0),
               [(0.0, 0.0)],
               [(-8.0, 8.0)]]]],
            2,
            10.0,
            -10.0,
            0,
            turn=1)

    def test_get_move(self):
        self.assertEqual(1, self.agent_1.get_move(self.tree_1)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_1)._index)
        self.assertEqual(1, self.agent_1.get_move(self.tree_2)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_2)._index)
        self.assertEqual(1, self.agent_1.get_move(self.tree_3)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_3)._index)


class TestMaxnAgent(unittest.TestCase):

    def setUp(self):
        self.agent_1 = MaxnAgent(prune_enable=False,
                                 verbose=5)
        self.agent_2 = MaxnAgent(name='Pruning Maxn Agent',
                                 verbose=5)
        self.tree_1 = game.Tree(
            [(1.0, 1.0, 1.0),
             [(1.0, 4.0, 4.0),
              [(2.0, 3.0, 0.0)],
              [(1.0, 1.0, 0.0)]],
             [(0.0, 1.0, 2.0),
              [(4.0, 0.0, 4.0)],
              [(1.0, 1.0, 1.0)]]],
            3,
            4.0,
            0.0,
            9.0)
        self.tree_2 = game.Tree(
            [(7.0, -3.5, 6.0, 0.9),
             [(1.0, 7.0, 2.2, -5.0),
              [(1.0, 5.0, -9.5, 3.0),
               [(2.0, -8.0, 1.0, 2.0)],
               [(1.0, -7.2, 2.0, 4.0)],
               [(-2.0, 0.4, 4.0, 5.0)]],
              [(-2.3, 2.0, -2.0, 3.0)]],
             [(2.1, 2.0, -1.1, 0.5)]],
            4,
            7.0,
            -9.5,
            10.4)
        self.tree_3 = game.Tree(
            [(3.0, -3.0),
             [(2.4, -2.4),
              [(5.0, -5.0),
               [(-10.0, 10.0)],
               [(-8.0, 8.0)],
               [(4.0, -4.0)]],
              [(-8.0, 8.0),
               [(3.0, -3.0)],
               [(5.0, -5.0)],
               [(-2.0, 2.0)]],
              [(-5.0, 5.0)]],
             [(-3.0, 3.0),
              [(0.0, 0.0)],
              [(1.0, -1.0)],
              [(4.0, -4.0),
               [(0.0, 0.0)],
               [(-8.0, 8.0)]]]],
            2,
            10.0,
            -10.0,
            0,
            turn=1)

    def test_get_move(self):
        self.assertEqual(1, self.agent_1.get_move(self.tree_1)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_1)._index)
        self.assertEqual(2, self.agent_1.get_move(self.tree_2)._index)
        self.assertEqual(2, self.agent_2.get_move(self.tree_2)._index)
        self.assertEqual(1, self.agent_1.get_move(self.tree_3)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_3)._index)


class TestParanoidAgent(unittest.TestCase):

    def setUp(self):
        self.agent_1 = ParanoidAgent(prune_enable=False,
                                     verbose=5)
        self.agent_2 = ParanoidAgent(name='Pruning Maxn Agent',
                                     verbose=5)
        self.tree_1 = game.Tree(
            [(1.0, 1.0, 1.0),
             [(1.0, 4.0, 4.0),
              [(2.0, 3.0, 0.0)],
              [(1.0, 1.0, 0.0)]],
             [(0.0, 1.0, 2.0),
              [(4.0, 0.0, 4.0)],
              [(1.0, 1.0, 1.0)]]],
            3,
            4.0,
            0.0,
            9.0)
        self.tree_2 = game.Tree(
            [(7.0, -3.5, 6.0, 0.9),
             [(1.0, 7.0, 2.2, -5.0),
              [(1.0, 5.0, -9.5, 3.0),
               [(2.0, -8.0, 1.0, 2.0)],
               [(1.0, -7.2, 2.0, 4.0)],
               [(-2.0, 0.4, 4.0, 5.0)]],
              [(-2.3, 2.0, -2.0, 3.0)]],
             [(2.1, 2.0, -1.1, 0.5)]],
            4,
            7.0,
            -9.5,
            10.4)
        self.tree_3 = game.Tree(
            [(3.0, -3.0),
             [(2.4, -2.4),
              [(5.0, -5.0),
               [(-10.0, 10.0)],
               [(-8.0, 8.0)],
               [(4.0, -4.0)]],
              [(-8.0, 8.0),
               [(3.0, -3.0)],
               [(5.0, -5.0)],
               [(-2.0, 2.0)]],
              [(-5.0, 5.0)]],
             [(-3.0, 3.0),
              [(0.0, 0.0)],
              [(1.0, -1.0)],
              [(4.0, -4.0),
               [(0.0, 0.0)],
               [(-8.0, 8.0)]]]],
            2,
            10.0,
            -10.0,
            0,
            turn=1)

    def test_get_move(self):
        self.assertEqual(1, self.agent_1.get_move(self.tree_1)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_1)._index)
        self.assertEqual(2, self.agent_1.get_move(self.tree_2)._index)
        self.assertEqual(2, self.agent_2.get_move(self.tree_2)._index)
        self.assertEqual(1, self.agent_1.get_move(self.tree_3)._index)
        self.assertEqual(1, self.agent_2.get_move(self.tree_3)._index)
