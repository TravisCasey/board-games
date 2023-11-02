"""
Unit testing for pyplayergames\\games\\checkers.
"""
# pylint: disable=C0115, C0116, C0413, W0212, W0104

# Temp code
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

import random
import pytest
import numpy as np
import pyplayergames as ppg


class TestCheckersUtilFunctions():

    @pytest.mark.parametrize('square, num',
                             [((0, 1), 1), ((4, 7), 20), ((5, 2), 22)])
    def test_coord_to_num(self, square, num):
        assert ppg.checkers.coord_to_num(square) == num

    @pytest.mark.parametrize('start, d, end',
                             [((0, 1), (1, 1), (1, 2)),
                              ((3, 6), (-1, 1), (2, 7))])
    def test_coord_sum(self, start, d, end):
        assert ppg.checkers.coord_sum(start, d) == end


class TestCheckersMove():

    @pytest.mark.parametrize('start, d, capt, string',
                             [((7, 6), (-1, -1), True, '32x27'),
                              ((4, 1), (1, -1), False, '17-21')])
    def test_move_string(self, start, d, capt, string):
        move = ppg.checkers.Move(start, d, capt)
        assert str(move) == string


class TestCheckersGamestate():

    @pytest.fixture()
    def board_1(self):
        return np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  2,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0, -2],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        )

    @pytest.fixture()
    def board_2(self):
        return np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  2,  0,  0],
             [0,  0,  0,  0,  0,  0,  1,  0],
             [0,  0,  0,  0,  0,  0,  0, -1],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        )

    @pytest.fixture()
    def board_3(self):
        return np.asarray(
            [[0,  0,  0,  0,  0,  0,  0, -2],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0, -1,  0,  0,  0, -1,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        )

    @pytest.fixture()
    def board_4(self):
        return np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  1,  0,  2,  0,  2,  0],
             [0,  0,  0, -1,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0, -1,  0,  0,  0, -1,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        )

    @pytest.fixture()
    def board_5(self):
        return np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0, -1,  0, -1,  0, -2,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0, -1,  0,  1,  0],
             [0,  0,  0,  2,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  2,  0],
             [0,  0,  0,  0,  0, -1,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        )

    @pytest.fixture()
    def board_list(self, board_1, board_2, board_3, board_4, board_5):
        return [None, board_1, board_2, board_3, board_4, board_5]

    @pytest.fixture()
    def gamestate(self, board_list, request):
        param_dict = request.param.copy()
        if 'board' in param_dict.keys():
            param_dict['board'] = board_list[param_dict['board']]
        return ppg.checkers.Gamestate(**param_dict)

    gamestate_param = [
        {},
        {'board': 1},
        {'board': 1, 'turn': 1},
        {'board': 1, 'plys_since_cap': 80},
        {'board': 2},
        {'board': 2, 'turn': 1},
        {'board': 3},
        {'board': 4, 'last_piece': (1, 4)},
        {'board': 4, 'turn': 1},
        {'board': 5},
        {'board': 5, 'turn': 1}
    ]

    # Move and Gamestate generation

    square_list = [
        [(2, 1),
         (1, 4),
         (0, 7),
         (4, 3),
         (5, 0)],
        [(0, 1),
         (3, 2),
         (4, 7)],
        [(3, 2),
         (4, 7)],
        [(3, 2),
         (4, 7)],
        [(2, 5),
         (3, 6),
         (4, 7)],
        [(2, 5),
         (3, 6),
         (4, 7)],
        [(0, 7),
         (6, 1),
         (6, 5)],
        [(1, 2),
         (1, 4),
         (1, 6)],
        [(2, 3),
         (6, 1),
         (6, 5)],
        [(3, 6),
         (4, 3),
         (5, 6)],
        [(1, 2),
         (1, 4),
         (1, 6),
         (3, 4),
         (6, 5)]
    ]

    d_list = [
        [([(1, -1), (1, 1)], []),
         ([], []),
         ([], []),
         ([], []),
         ([], [])],
        [([], []),
         ([(-1, -1), (-1, 1), (1, -1), (1, 1)], []),
         ([], [])],
        [([], []),
         ([(-1, -1), (1, -1)], [])],
        [([(-1, -1), (-1, 1), (1, -1), (1, 1)], []),
         ([], [])],
        [([(-1, -1), (-1, 1), (1, -1)], []),
         ([(1, -1)], []),
         ([], [])],
        [([], []),
         ([], []),
         ([], [])],
        [([], []),
         ([], []),
         ([], [])],
        [([(1, -1)], [(1, 1)]),
         ([(-1, -1), (-1, 1), (1, 1)], [(1, -1)]),
         ([(-1, -1), (-1, 1), (1, -1), (1, 1)], [])],
        [([], [(-1, -1), (-1, 1)]),
         ([(-1, -1), (-1, 1)], []),
         ([(-1, -1), (-1, 1)], [])],
        [([(1, -1), (1, 1)], []),
         ([(-1, -1), (1, -1), (1, 1)], [(-1, 1)]),
         ([(-1, -1), (-1, 1), (1, 1)], [(1, -1)])],
        [([(-1, -1), (-1, 1)], []),
         ([(-1, -1), (-1, 1)], []),
         ([(-1, -1), (-1, 1), (1, -1), (1, 1)], []),
         ([(-1, -1), (-1, 1)], []),
         ([(-1, -1)], [(-1, 1)])]
    ]

    @pytest.mark.parametrize('gamestate, squares, ds',
                             tuple(zip(gamestate_param, square_list, d_list)),
                             indirect=['gamestate'])
    def test_piece_moves(self, gamestate, squares, ds):
        for ind, square in enumerate(squares):
            move_tup = gamestate.piece_moves(square)
            move_tup = ([move.d for move in move_tup[0]],
                        [move.d for move in move_tup[1]])
            assert move_tup == ds[ind]

    valid_square_list = [
        [(2, 1), (2, 1), (2, 3), (2, 3), (2, 5), (2, 5), (2, 7)],
        [(3, 2), (3, 2), (3, 2), (3, 2)],
        [(4, 7), (4, 7)],
        [(3, 2), (3, 2), (3, 2), (3, 2)],
        [(2, 5), (2, 5), (2, 5), (3, 6)],
        [],
        [],
        [(1, 4)],
        [(2, 3), (2, 3)],
        [(4, 3), (5, 6)],
        [(6, 5)]
    ]

    valid_d_list = [
        [(1, -1), (1, 1), (1, -1), (1, 1), (1, -1), (1, 1), (1, -1)],
        [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        [(-1, -1), (1, -1)],
        [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        [(-1, -1), (-1, 1), (1, -1), (1, -1)],
        [],
        [],
        [(1, -1)],
        [(-1, -1), (-1, 1)],
        [(-1, 1), (1, -1)],
        [(-1, 1)]
    ]

    @pytest.mark.parametrize('gamestate, squares, ds',
                             tuple(zip(gamestate_param,
                                       valid_square_list,
                                       valid_d_list)),
                             indirect=['gamestate'])
    def test_valid_moves(self, gamestate, squares, ds):
        assert squares == [move.start for move in gamestate.valid_moves]
        assert ds == [move.d for move in gamestate.valid_moves]

    next_move_list = [
        ppg.checkers.Move((2, 5), (1, -1), False),
        ppg.checkers.Move((3, 2), (-1, 1), False),
        ppg.checkers.Move((4, 7), (-1, -1), False),
        ppg.checkers.Move((3, 2), (1, 1), False),
        ppg.checkers.Move((3, 6), (1, -1), False),
        None,
        None,
        ppg.checkers.Move((1, 4), (1, -1), True),
        ppg.checkers.Move((2, 3), (-1, 1), True),
        ppg.checkers.Move((4, 3), (-1, 1), True),
        ppg.checkers.Move((6, 5), (-1, 1), True)
    ]

    next_board_list = [
        np.asarray(
            [[0,  1,  0,  1,  0,  1,  0,  1],
             [1,  0,  1,  0,  1,  0,  1,  0],
             [0,  1,  0,  1,  0,  0,  0,  1],
             [0,  0,  0,  0,  1,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [-1, 0, -1,  0, -1,  0, -1,  0],
             [0, -1,  0, -1,  0, -1,  0, -1],
             [-1, 0, -1,  0, -1,  0, -1,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  2,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0, -2],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  2,  0,  0,  0, -2,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  2,  0,  0,  0, -2],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  2,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  1,  0, -1],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        None,
        None,
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  1,  0,  0,  0,  2,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  2,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0, -1,  0,  0,  0, -1,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0, -2,  0,  0],
             [0,  0,  1,  0,  0,  0,  2,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0, -1,  0,  0,  0, -1,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0, -1,  0, -1,  0, -2,  0],
             [0,  0,  0,  0,  0,  2,  0,  0],
             [0,  0,  0,  0,  0,  0,  1,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  2,  0],
             [0,  0,  0,  0,  0, -1,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        ),
        np.asarray(
            [[0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0, -1,  0, -1,  0, -2,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0, -1,  0,  1,  0],
             [0,  0,  0,  2,  0,  0,  0, -1],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0]]
        )
    ]

    @pytest.mark.parametrize('gamestate, move, board',
                             tuple(zip(gamestate_param,
                                       next_move_list,
                                       next_board_list)),
                             indirect=['gamestate'])
    def test_get_next_board(self, gamestate, move, board):
        if move is not None:
            hash_ini = hash(gamestate)
            board_ini = np.copy(gamestate.board)
            assert np.array_equal(gamestate.get_next(move).board, board), (
                'New attribute board incorrect.'
            )
            assert hash_ini == hash(gamestate), (
                'Hash failed to reset correctly.'
            )
            assert np.array_equal(gamestate.board, board_ini), (
                'Attribute board failed to reset correctly.'
            )

    next_turn_list = [
        1,
        1,
        0,
        1,
        1,
        None,
        None,
        1,
        0,
        0,
        1
    ]
    @pytest.mark.parametrize('gamestate, move, turn',
                             tuple(zip(gamestate_param,
                                       next_move_list,
                                       next_turn_list)),
                             indirect=['gamestate'])
    def test_get_next_turn(self, gamestate, move, turn):
        if move is not None:
            assert gamestate.get_next(move).turn == turn, (
                'New attribute turn incorrect.'
            )

    next_plys_since_cap = [
        1,
        1,
        1,
        81,
        1,
        None,
        None,
        0,
        0,
        0,
        0
    ]

    @pytest.mark.parametrize('gamestate, move, plys_since_cap',
                             tuple(zip(gamestate_param,
                                       next_move_list,
                                       next_plys_since_cap)),
                             indirect=['gamestate'])
    def test_get_next_plys_since_cap(self, gamestate, move, plys_since_cap):
        if move is not None:
            assert gamestate.get_next(move).plys_since_cap == plys_since_cap, (
                'New attribute plys_since_cap incorrect.'
            )

    # Terminal states, scoring, reward

    score_list = [
        (0.0, 0.0),
        (10.0, -10.0),
        (10.0, -10.0),
        (0.0, 0.0),
        (49997020.0, -49997020.0),
        (float('inf'), float('-inf')),
        (float('-inf'), float('inf')),
        (39394030.0, -39394030.0),
        (39394030.0, -39394030.0),
        (-41391972.0, 41391972.0),
        (-41391972.0, 41391972.0)
    ]

    @pytest.mark.parametrize('gamestate, score',
                             tuple(zip(gamestate_param, score_list)),
                             indirect=['gamestate'])
    def test_score(self, gamestate, score):
        assert gamestate.score == score

    winner_list = [
        None,
        None,
        None,
        -1,
        None,
        0,
        1,
        None,
        None,
        None,
        None
    ]

    @pytest.mark.parametrize('gamestate, winner',
                             tuple(zip(gamestate_param, winner_list)),
                             indirect=['gamestate'])
    def test_winner(self, gamestate, winner):
        assert gamestate.winner == winner

    game_over_list = [
        False,
        False,
        False,
        True,
        False,
        True,
        True,
        False,
        False,
        False,
        False
    ]

    @pytest.mark.parametrize('gamestate, game_over',
                             tuple(zip(gamestate_param, game_over_list)),
                             indirect=['gamestate'])
    def test_is_game_over(self, gamestate, game_over):
        assert gamestate.is_game_over() is game_over

    reward_list = [
        None,
        None,
        None,
        (0.5, 0.5),
        None,
        (1.0, 0.0),
        (0.0, 1.0),
        None,
        None,
        None,
        None
    ]

    @pytest.mark.parametrize('gamestate, reward',
                             tuple(zip(gamestate_param, reward_list)),
                             indirect=['gamestate'])
    def test_reward(self, gamestate, reward):
        if reward is None:
            with pytest.raises(AttributeError):
                gamestate.reward
        else:
            assert gamestate.reward == reward

    # Hashing

    @pytest.mark.parametrize('gamestate', gamestate_param, indirect=True)
    def test_hash_key_instantiation(self, gamestate):
        max_value = 2**gamestate._hash_length
        for square in gamestate._SQUARES:
            for piece in (-2, -1, 1, 2):
                hash_value = gamestate._hash_key[square][piece]
                assert isinstance(hash_value, int), (
                    f'hash key at {square}, {piece} not an integer.'
                )
                assert hash_value < max_value, (
                    f'hash key at {square}, {piece} too large.'
                )
                assert hash_value >= 0, (
                    f'hash key at {square}, {piece} negative.'
                )

    @pytest.mark.parametrize('gamestate', gamestate_param, indirect=True)
    def test_hash(self, gamestate):
        max_value = 2**gamestate._hash_length
        assert (hash(gamestate) > 0 and hash(gamestate) < max_value), (
            'hash too large or negative.'
        )

    @pytest.mark.parametrize('gamestate', gamestate_param, indirect=True)
    def test_board_update_hash(self, gamestate):
        # Runs more than once to avoid hash overlap issues.
        iterations = 10
        threshold= 2
        errors = 0
        original_hash = hash(gamestate)
        for _ in range(iterations):
            square = random.choice(gamestate._SQUARES)
            piece = gamestate.board[square]
            new_piece = random.choice((-2, -1, 0, 1, 2))
            gamestate.update_board(square, new_piece)
            if piece == new_piece:
                assert hash(gamestate) == original_hash, (
                    'Identical board position has different hash.'
                )
            elif hash(gamestate) == original_hash:
                errors += 1
            gamestate.update_board(square, piece)
            assert hash(gamestate) == original_hash, (
                'Identical board position has different hash.'
            )
        assert errors < threshold, (
            'Board update hashing improperly.'
        )

    def test_same_position_same_hash(self, board_1):
        moves = (ppg.checkers.Move((3, 2), (1, 1), False),
                 ppg.checkers.Move((4, 7), (1, -1), False),
                 ppg.checkers.Move((4, 3), (-1, -1), False),
                 ppg.checkers.Move((5, 6), (-1, 1), False))
        gamestate = ppg.checkers.Gamestate(board=board_1)
        hash_ini = hash(gamestate)
        for move in moves:
            gamestate = gamestate.get_next(move)
        assert hash(gamestate) == hash_ini, (
            'Identical board position has different hash.'
        )

        moves = (ppg.checkers.Move((4, 7), (-1, -1), False),
                 ppg.checkers.Move((3, 2), (1, -1), False),
                 ppg.checkers.Move((3, 6), (1, 1), False),
                 ppg.checkers.Move((4, 1), (-1, 1), False))
        gamestate = ppg.checkers.Gamestate(board=board_1, turn=1)
        hash_ini = hash(gamestate)
        for move in moves:
            gamestate = gamestate.get_next(move)
        assert hash(gamestate) == hash_ini, (
            'Identical board position has different hash.'
        )
