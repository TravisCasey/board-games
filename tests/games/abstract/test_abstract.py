"""Unit testing module for pyboardgames/games/abstract/game.py."""

import unittest
from context import game


class TestEdge(unittest.TestCase):

    def setUp(self):
        self.move_1 = game.Edge(1)
        self.move_2 = game.Edge(2)
        self.move_3 = game.Edge(3)

    def test_init(self):
        with self.assertRaises(TypeError):
            game.Edge('1')
            game.Edge(0.0)
        with self.assertRaises(ValueError):
            game.Edge(0)
            game.Edge(-2)

    def test_str(self):
        self.assertEqual(str(self.move_1), '1')
        self.assertEqual(str(self.move_2), '2')

    def test_int(self):
        self.assertEqual(int(self.move_1), 1)
        self.assertEqual(int(self.move_2), 2)


class TestTree(unittest.TestCase):

    def setUp(self):
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
        self.move_1 = game.Edge(1)
        self.move_2 = game.Edge(2)
        self.move_3 = game.Edge(3)

    def test_get_next(self):
        new_tree_1 = self.tree_1.get_next(self.move_1)
        self.assertIsInstance(new_tree_1, game.Tree)
        self.assertEqual(new_tree_1.tree,
                         [(1.0, 4.0, 4.0),
                          [(2.0, 3.0, 0.0)],
                          [(1.0, 1.0, 0.0)]])
        self.assertEqual(new_tree_1.turn, 1)
        new_tree_2 = new_tree_1.get_next(self.move_2)
        self.assertIsInstance(new_tree_2, game.Tree)
        self.assertEqual(new_tree_2.tree,
                         [(1.0, 1.0, 0.0)])
        self.assertEqual(new_tree_2.turn, 2)

        new_tree_3 = self.tree_2.get_next(self.move_2)
        self.assertIsInstance(new_tree_3, game.Tree)
        self.assertEqual(new_tree_3.tree,
                         [(2.1, 2.0, -1.1, 0.5)])
        self.assertEqual(new_tree_3.turn, 1)

        new_tree_4 = self.tree_3.get_next(self.move_1)
        new_tree_5 = new_tree_4.get_next(self.move_2)
        new_tree_6 = new_tree_5.get_next(self.move_3)
        self.assertIsInstance(new_tree_4, game.Tree)
        self.assertIsInstance(new_tree_5, game.Tree)
        self.assertIsInstance(new_tree_6, game.Tree)
        self.assertEqual(new_tree_4.tree,
                         [(2.4, -2.4),
                          [(5.0, -5.0),
                           [(-10.0, 10.0)],
                           [(-8.0, 8.0)],
                           [(4.0, -4.0)]],
                          [(-8.0, 8.0),
                           [(3.0, -3.0)],
                           [(5.0, -5.0)],
                           [(-2.0, 2.0)]],
                          [(-5.0, 5.0)]])
        self.assertEqual(new_tree_5.tree,
                         [(-8.0, 8.0),
                          [(3.0, -3.0)],
                          [(5.0, -5.0)],
                          [(-2.0, 2.0)]])
        self.assertEqual(new_tree_6.tree,
                         [(-2, 2)])
        self.assertEqual(self.tree_3.turn, 1)
        self.assertEqual(new_tree_4.turn, 0)
        self.assertEqual(new_tree_5.turn, 1)
        self.assertEqual(new_tree_6.turn, 0)

    def test_valid_moves(self):
        new_tree_1 = self.tree_1.get_next(self.move_2)
        new_tree_2 = self.tree_2.get_next(self.move_2)
        new_tree_3 = self.tree_3.get_next(self.move_2)

        self.assertEqual([int(edge) for edge in self.tree_1.valid_moves],
                         [1, 2])
        self.assertEqual([int(edge) for edge in self.tree_2.valid_moves],
                         [1, 2])
        self.assertEqual([int(edge) for edge in self.tree_3.valid_moves],
                         [1, 2])
        self.assertEqual([int(edge) for edge in new_tree_1.valid_moves],
                         [1, 2])
        self.assertEqual([int(edge) for edge in new_tree_2.valid_moves],
                         [])
        self.assertEqual([int(edge) for edge in new_tree_3.valid_moves],
                         [1, 2, 3])

    def test_is_game_over(self):
        new_tree_1 = self.tree_1.get_next(self.move_1)
        new_tree_2 = new_tree_1.get_next(self.move_2)
        new_tree_3 = self.tree_2.get_next(self.move_2)
        new_tree_4 = self.tree_3.get_next(self.move_1)
        new_tree_5 = new_tree_4.get_next(self.move_2)
        new_tree_6 = new_tree_4.get_next(self.move_3)

        self.assertFalse(self.tree_1.is_game_over())
        self.assertFalse(self.tree_2.is_game_over())
        self.assertFalse(self.tree_3.is_game_over())
        self.assertFalse(new_tree_1.is_game_over())
        self.assertTrue(new_tree_2.is_game_over())
        self.assertTrue(new_tree_3.is_game_over())
        self.assertFalse(new_tree_4.is_game_over())
        self.assertFalse(new_tree_5.is_game_over())
        self.assertTrue(new_tree_6.is_game_over())

    def test_score(self):
        new_tree_1 = self.tree_1.get_next(self.move_1)
        new_tree_2 = new_tree_1.get_next(self.move_2)
        new_tree_3 = self.tree_2.get_next(self.move_2)
        new_tree_4 = self.tree_3.get_next(self.move_1)
        new_tree_5 = new_tree_4.get_next(self.move_2)
        new_tree_6 = new_tree_4.get_next(self.move_3)

        self.assertEqual(self.tree_1.score, (1.0, 1.0, 1.0))
        self.assertEqual(self.tree_2.score, (7.0, -3.5, 6.0, 0.9))
        self.assertEqual(self.tree_3.score, (3.0, -3.0))
        self.assertEqual(new_tree_1.score, (1.0, 4.0, 4.0))
        self.assertEqual(new_tree_2.score, (1.0, 1.0, 0.0))
        self.assertEqual(new_tree_3.score, (2.1, 2.0, -1.1, 0.5))
        self.assertEqual(new_tree_4.score, (2.4, -2.4))
        self.assertEqual(new_tree_5.score, (-8.0, 8.0))
        self.assertEqual(new_tree_6.score, (-5.0, 5.0))
