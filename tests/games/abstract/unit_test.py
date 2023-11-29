"""
Unit testing for pyplayergames\\games\\abstract
"""
# pylint: disable=C0115, C0116, C0413, W0212, W0104, R0904

# Temp code
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

import pytest
import pyplayergames as ppg


class TestEdge():

    @pytest.mark.parametrize('index', [0, 2, 14, 3])
    def test_edge_index_access(self, index):
        assert int(ppg.abstract.Edge(index)) == index

    @pytest.mark.parametrize('index', ['one', 14.0, -3])
    def test_constructor_errors(self, index):
        with pytest.raises((TypeError, ValueError)):
            ppg.abstract.Edge(index)

    @pytest.mark.parametrize('index, string',
                             [(1, '1'), (3, '3'), (400, '400')])
    def test_edge_string(self, index, string):
        assert str(ppg.abstract.Edge(index)) == string


class TestNode():

    @pytest.fixture()
    def node_0(self):
        tree_list =  [0, (0.0, 0.0),
                      [1, (2.0, -2.0),
                       [0, (3.0, -3.0),
                        [1, (float('inf'), float('-inf'))],
                        [1, (float('-inf'), float('inf'))],
                        [1, (-2.0, 2.0)]],
                       [0, (2.0, -2.0),
                        [1, (-3.0, 3.0)],
                        [1, (0.0, 0.0)]]],
                      [1, (1.0, -1.0),
                       [0, (-1.0, 1.0)],
                       [0, (-2.0, 2.0)]]
                      ]
        return ppg.abstract.Node.build_tree(
            2,
            -3.0,
            0.0,
            *tree_list
        )

    @pytest.fixture()
    def node_1(self):
        tree_list =  [2, (1.5, 2.0, 0.0, 4.0),
                      [1, (2.0, -2.0, 2.0, -2.0),
                       [0, (3.0, -3.0, 0.5, 2.5)],
                       [0, (2.0, -2.0, -0.5, 2.2),
                        [1, (-3.0, 3.0, 3.0, 3.0),
                         [2, (-1.5, 1.5, 0.5, 4.5)],
                         [2, (1.0, 1.0, 1.0, -1.0)]],
                        [1, (0.0, 0.0, 0.0, 0.0)]]],
                      [1, (1.0, -1.0, 0.4, 2.2)]
                      ]
        return ppg.abstract.Node.build_tree(
            4,
            -3.0,
            7.5,
            *tree_list
        )

    @pytest.fixture()
    def node_list(self, node_0, node_1):
        return [node_0, node_1]

    @pytest.fixture()
    def node(self, node_list, request):
        param_dict = request.param.copy()
        node = node_list[param_dict['node']]
        if 'moves' in param_dict:
            for move in param_dict['moves']:
                node = node.get_next(ppg.abstract.Edge(move))
        return node

    node_param = [
        {'node': 0},
        {'node': 0, 'moves': (0,)},
        {'node': 0, 'moves': (0, 0, 0)},
        {'node': 0, 'moves': (0, 0, 1)},
        {'node': 0, 'moves': (1, 1)},
        {'node': 1},
        {'node': 1, 'moves': (0, 1, 0)},
        {'node': 1, 'moves': (0, 1, 0, 1)}
    ]

    move_int_list = [
        (0, 1),
        (0, 1),
        tuple(),
        tuple(),
        tuple(),
        (0, 1),
        (0, 1),
        tuple()
    ]

    @pytest.mark.parametrize('node, move_ints',
                             tuple(zip(node_param, move_int_list)),
                             indirect=['node'])
    def test_get_moves(self, node, move_ints):
        assert tuple(int(move) for move in node.get_moves()) == move_ints

    move_list = [
        0,
        1,
        None,
        None,
        None,
        1,
        0,
        None
    ]

    turn_list = [
        1,
        0,
        1,
        1,
        0,
        1,
        2,
        2
    ]

    score_list = [
        (2.0, -2.0),
        (2.0, -2.0),
        (float('inf'), float('-inf')),
        (float('-inf'), float('inf')),
        (-2.0, 2.0),
        (1.0, -1.0, 0.4, 2.2),
        (-1.5, 1.5, 0.5, 4.5),
        (1.0, 1.0, 1.0, -1.0)
    ]

    @pytest.mark.parametrize('node, move, turn, score',
                             tuple(zip(node_param,
                                       move_list,
                                       turn_list,
                                       score_list)),
                             indirect=['node'])
    def test_get_next(self, node, move, turn, score):
        if move is None:
            next_node = node
        else:
            next_node = node.get_next(ppg.abstract.Edge(move))
        assert next_node.turn == turn
        assert next_node.get_score() == score

    game_over_list = [
        False,
        False,
        True,
        True,
        True,
        False,
        False,
        True
    ]

    @pytest.mark.parametrize('node, game_over',
                             tuple(zip(node_param, game_over_list)),
                             indirect=['node'])
    def test_is_game_over(self, node, game_over):
        assert node.is_game_over() == game_over

    reward_list = [
        None,
        None,
        (1.0, 0.0),
        (0.0, 1.0),
        (0.0, 1.0),
        None,
        None,
        (1.0/3, 1.0/3, 1.0/3, 0.0)
    ]

    @pytest.mark.parametrize('node, reward',
                             tuple(zip(node_param, reward_list)),
                             indirect=['node'])
    def test_get_reward(self, node, reward):
        if reward is None:
            with pytest.raises(AttributeError):
                node.get_reward()
        else:
            assert node.get_reward() == reward
