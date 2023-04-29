"""Unit testing module for pyboardgames/games/checkers/game.py."""

import unittest
import numpy as np
from context import game


class TestCheckersMove(unittest.TestCase):

    def setUp(self):
        self.move_1 = game.CheckersMove(((0, 1), (2, 3),
                                        (4, 5), (6, 7)))
        self.move_2 = game.CheckersMove(((2, 1), (3, 0)))

    def test_init(self):
        with self.assertRaises(TypeError):
            game.CheckersMove(8)
            game.CheckersMove(True)
            game.CheckersMove((2, 4))
        with self.assertRaises(ValueError):
            game.CheckersMove(((2, 4), (7, 3, 1)))
            game.CheckersMove((2, 4), (8, -1))

    def test_length(self):
        self.assertEqual(len(self.move_1), 4)
        self.assertEqual(len(self.move_2), 2)

    def test_getitem(self):
        self.assertEqual(self.move_1[0], (0, 1))
        self.assertEqual(self.move_1[1], (2, 3))
        self.assertEqual(self.move_1[2], (4, 5))
        self.assertEqual(self.move_1[3], (6, 7))
        self.assertEqual(self.move_2[0], (2, 1))
        self.assertEqual(self.move_2[1], (3, 0))
        self.assertEqual(self.move_1[-1], (6, 7))
        self.assertEqual(self.move_1[2:], ((4, 5), (6, 7)))
        self.assertEqual(self.move_2[2:], ())
        with self.assertRaises(IndexError):
            self.move_1[4]
            self.move_2[3:]
        with self.assertRaises(TypeError):
            self.move_1['one':'three']
            self.move_2[True]


class TestCheckersGamestate(unittest.TestCase):

    def setUp(self):
        self.gamestate_1 = game.CheckersGamestate()
        self.move_1 = game.CheckersMove(((2, 1), (3, 0)))
        self.move_2 = game.CheckersMove(((2, 1), (3, 2)))
        self.move_3 = game.CheckersMove(((5, 2), (4, 1)))
        self.move_4 = game.CheckersMove(((5, 2), (4, 3)))
        self.move_5 = game.CheckersMove(((2, 6), (3, 5)))
        self.move_6 = game.CheckersMove(((2, 6), (1, 7)))
        self.gamestate_2 = game.CheckersGamestate(board=np.asarray(
            [[0,  0,  0,  0,  0,  1,  0,  0],
             [0,  0,  1,  0,  1,  0,  0,  0],
             [0,  0,  0, -1,  0,  0,  0,  0],
             [0,  0,  1,  0,  0,  0,  2,  0],
             [0, -1,  0,  0,  0,  0,  0,  0],
             [0,  0, -1,  0,  1,  0,  1,  0],
             [0, -1,  0, -1,  0, -2,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ))
        self.move_7 = game.CheckersMove(((1, 2), (2, 1)))
        self.move_8 = game.CheckersMove(((1, 2), (2, 3)))
        self.move_9 = game.CheckersMove(((1, 2), (3, 4)))
        self.move_10 = game.CheckersMove(((1, 4), (3, 2)))
        self.move_11 = game.CheckersMove(((1, 4), (3, 2), (5, 0)))
        self.move_12 = game.CheckersMove(((1, 4), (3, 2), (4, 3)))
        self.move_13 = game.CheckersMove(((3, 2), (5, 0)))
        self.move_14 = game.CheckersMove(((3, 2), (5, 0), (7, 2)))
        self.move_15 = game.CheckersMove(((5, 4), (7, 2)))
        self.move_16 = game.CheckersMove(((5, 4), (7, 6)))
        self.move_17 = game.CheckersMove(((5, 6), (7, 4)))
        self.move_18 = game.CheckersMove(((3, 2), (6, 0)))
        self.move_19 = game.CheckersMove(((3, 2), (5, 0), (6, 2)))
        self.move_20 = game.CheckersMove(((3, 6), (1, 7)))
        self.move_21 = game.CheckersMove(((2, 3), (0, 1)))
        self.move_22 = game.CheckersMove(((2, 3), (0, 5)))
        self.move_23 = game.CheckersMove(((6, 5), (4, 7), (2, 5),
                                          (0, 3), (2, 1), (4, 3)))
        self.move_24 = game.CheckersMove(((6, 5), (4, 7), (2, 5),
                                          (0, 3), (2, 1), (4, 3),
                                          (2, 1)))
        self.move_25 = game.CheckersMove(((6, 5), (4, 7), (2, 5),
                                          (0, 3), (2, 1), (4, 3),
                                          (6, 5)))
        self.move_26 = game.CheckersMove(((6, 5), (4, 7), (2, 5),
                                          (0, 3), (2, 1), (4, 3),
                                          (4, 7)))
        self.move_27 = game.CheckersMove(((6, 5), (4, 3), (2, 1),
                                          (0, 3), (2, 5), (4, 7),
                                          (6, 5)))
        self.move_28 = game.CheckersMove(((6, 5), (4, 7), (2, 5)))
        self.move_29 = game.CheckersMove(((6, 5), (0, 3)))
        self.move_30 = game.CheckersMove(((6, 3), (4, 5), (2, 7)))
        self.gamestate_3 = game.CheckersGamestate(board=np.asarray(
            [[0, -2,  0,  0,  0,  0,  0,  0],
             [0,  0,  1,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  2,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0, -1,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0, -2,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ))
        self.move_31 = game.CheckersMove(((1, 2), (2, 1)))
        self.move_32 = game.CheckersMove(((1, 2), (2, 1), (3, 2)))
        self.move_33 = game.CheckersMove(((1, 2), (0, 3)))
        self.move_34 = game.CheckersMove(((1, 2), (3, 4)))
        self.move_35 = game.CheckersMove(((2, 5), (1, 4)))
        self.move_36 = game.CheckersMove(((2, 5), (1, 6), (0, 7)))
        self.move_37 = game.CheckersMove(((2, 5), (3, 6)))
        self.move_38 = game.CheckersMove(((4, 1), (3, 2)))
        self.move_39 = game.CheckersMove(((0, 1), (2, 3)))
        self.move_40 = game.CheckersMove(((0, 1), (1, 0)))

    def test_jumps(self):
        self.assertEqual(self.gamestate_1.jumps((0, 1), 1), {})
        self.assertEqual(self.gamestate_1.jumps((2, 1), 1), {})
        self.assertEqual(self.gamestate_1.jumps((2, 1), -1), {})
        self.assertEqual(self.gamestate_1.jumps((1, 0), -2), {(3, 2): (2, 1)})
        self.assertEqual(self.gamestate_1.jumps((1, 0), -2), {(3, 2): (2, 1)})
        self.assertTrue(self.gamestate_1.jumps((1, 0), -2))
        self.assertFalse(self.gamestate_1.jumps((1, 0), -1))

        self.assertEqual(self.gamestate_2.jumps((1, 2), 1), {(3, 4): (2, 3)})
        self.assertEqual(self.gamestate_2.jumps((1, 4), 1), {})
        self.assertEqual(self.gamestate_2.jumps((5, 4), 1), {(7, 2): (6, 3),
                                                             (7, 6): (6, 5)})
        self.assertEqual(self.gamestate_2.jumps((5, 2), -1), {})
        self.assertEqual(self.gamestate_2.jumps((5, 2), 1), {(7, 0): (6, 1),
                                                             (7, 4): (6, 3)})

        self.assertEqual(self.gamestate_3.jumps((0, 1), -2), {(2, 3): (1, 2)})
        self.assertFalse(self.gamestate_3.jumps((0, 1), -1))
        self.assertFalse(self.gamestate_3.jumps((1, 2), 1))
        self.assertFalse(self.gamestate_3.jumps((1, 2), 2))
        self.assertFalse(self.gamestate_3.jumps((2, 5), 2))
        self.assertFalse(self.gamestate_3.jumps((2, 5), 1))
        self.assertFalse(self.gamestate_3.jumps((2, 5), -1))
        self.assertFalse(self.gamestate_3.jumps((2, 5), -2))

    def test_is_valid(self):
        self.assertTrue(self.gamestate_1.is_valid(self.move_1))
        self.assertTrue(self.gamestate_1.is_valid(self.move_2))
        self.assertFalse(self.gamestate_1.is_valid(self.move_3))
        self.assertFalse(self.gamestate_1.is_valid(self.move_4))
        self.assertFalse(self.gamestate_1.is_valid(self.move_5))
        self.assertFalse(self.gamestate_1.is_valid(self.move_6))
        self.gamestate_1.turn = -1
        self.assertFalse(self.gamestate_1.is_valid(self.move_1))
        self.assertFalse(self.gamestate_1.is_valid(self.move_2))
        self.assertTrue(self.gamestate_1.is_valid(self.move_3))
        self.assertTrue(self.gamestate_1.is_valid(self.move_4))
        self.assertFalse(self.gamestate_1.is_valid(self.move_5))
        self.assertFalse(self.gamestate_1.is_valid(self.move_6))

        self.assertFalse(self.gamestate_2.is_valid(self.move_7))
        self.assertFalse(self.gamestate_2.is_valid(self.move_8))
        self.assertTrue(self.gamestate_2.is_valid(self.move_9))
        self.assertFalse(self.gamestate_2.is_valid(self.move_10))
        self.assertFalse(self.gamestate_2.is_valid(self.move_11))
        self.assertFalse(self.gamestate_2.is_valid(self.move_12))
        self.assertFalse(self.gamestate_2.is_valid(self.move_13))
        self.assertTrue(self.gamestate_2.is_valid(self.move_14))
        self.assertTrue(self.gamestate_2.is_valid(self.move_15))
        self.assertTrue(self.gamestate_2.is_valid(self.move_16))
        self.assertTrue(self.gamestate_2.is_valid(self.move_17))
        self.assertFalse(self.gamestate_2.is_valid(self.move_18))
        self.assertFalse(self.gamestate_2.is_valid(self.move_19))
        self.assertFalse(self.gamestate_2.is_valid(self.move_20))
        self.assertFalse(self.gamestate_2.is_valid(self.move_21))
        self.assertFalse(self.gamestate_2.is_valid(self.move_22))
        self.assertFalse(self.gamestate_2.is_valid(self.move_23))
        self.assertFalse(self.gamestate_2.is_valid(self.move_24))
        self.assertFalse(self.gamestate_2.is_valid(self.move_25))
        self.assertFalse(self.gamestate_2.is_valid(self.move_26))
        self.assertFalse(self.gamestate_2.is_valid(self.move_27))
        self.assertFalse(self.gamestate_2.is_valid(self.move_28))
        self.assertFalse(self.gamestate_2.is_valid(self.move_29))
        self.assertFalse(self.gamestate_2.is_valid(self.move_30))
        self.gamestate_2.turn = -1
        self.assertFalse(self.gamestate_2.is_valid(self.move_7))
        self.assertFalse(self.gamestate_2.is_valid(self.move_8))
        self.assertFalse(self.gamestate_2.is_valid(self.move_9))
        self.assertFalse(self.gamestate_2.is_valid(self.move_10))
        self.assertFalse(self.gamestate_2.is_valid(self.move_11))
        self.assertFalse(self.gamestate_2.is_valid(self.move_12))
        self.assertFalse(self.gamestate_2.is_valid(self.move_13))
        self.assertFalse(self.gamestate_2.is_valid(self.move_14))
        self.assertFalse(self.gamestate_2.is_valid(self.move_15))
        self.assertFalse(self.gamestate_2.is_valid(self.move_16))
        self.assertFalse(self.gamestate_2.is_valid(self.move_17))
        self.assertFalse(self.gamestate_2.is_valid(self.move_18))
        self.assertFalse(self.gamestate_2.is_valid(self.move_19))
        self.assertFalse(self.gamestate_2.is_valid(self.move_20))
        self.assertTrue(self.gamestate_2.is_valid(self.move_21))
        self.assertFalse(self.gamestate_2.is_valid(self.move_22))
        self.assertFalse(self.gamestate_2.is_valid(self.move_23))
        self.assertFalse(self.gamestate_2.is_valid(self.move_24))
        self.assertTrue(self.gamestate_2.is_valid(self.move_25))
        self.assertFalse(self.gamestate_2.is_valid(self.move_26))
        self.assertTrue(self.gamestate_2.is_valid(self.move_27))
        self.assertFalse(self.gamestate_2.is_valid(self.move_28))
        self.assertFalse(self.gamestate_2.is_valid(self.move_29))
        self.assertTrue(self.gamestate_2.is_valid(self.move_30))

        self.assertTrue(self.gamestate_3.is_valid(self.move_31))
        self.assertFalse(self.gamestate_3.is_valid(self.move_32))
        self.assertFalse(self.gamestate_3.is_valid(self.move_33))
        self.assertFalse(self.gamestate_3.is_valid(self.move_34))
        self.assertTrue(self.gamestate_3.is_valid(self.move_35))
        self.assertFalse(self.gamestate_3.is_valid(self.move_36))
        self.assertTrue(self.gamestate_3.is_valid(self.move_37))
        self.assertFalse(self.gamestate_3.is_valid(self.move_38))
        self.assertFalse(self.gamestate_3.is_valid(self.move_39))
        self.assertFalse(self.gamestate_3.is_valid(self.move_40))
        self.gamestate_3.turn = -1
        self.assertFalse(self.gamestate_3.is_valid(self.move_31))
        self.assertFalse(self.gamestate_3.is_valid(self.move_32))
        self.assertFalse(self.gamestate_3.is_valid(self.move_33))
        self.assertFalse(self.gamestate_3.is_valid(self.move_34))
        self.assertFalse(self.gamestate_3.is_valid(self.move_35))
        self.assertFalse(self.gamestate_3.is_valid(self.move_36))
        self.assertFalse(self.gamestate_3.is_valid(self.move_37))
        self.assertFalse(self.gamestate_3.is_valid(self.move_38))
        self.assertTrue(self.gamestate_3.is_valid(self.move_39))
        self.assertFalse(self.gamestate_3.is_valid(self.move_40))
