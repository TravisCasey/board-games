"""
Functional testing for pyplayergames\\games\\abstract
"""
# pylint: disable=C0115, C0116, C0413, W0212, W0104, R0904

# Temp code
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

import pytest
import pyplayergames as ppg


class TestAbstractRuns():

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
        {'node': 0, 'moves': (1, 1)},
        {'node': 1},
        {'node': 1, 'moves': (0, 1, 0)},
        {'node': 1, 'moves': (0, 1, 0, 1)}
    ]

    @pytest.mark.parametrize('node', node_param, indirect=['node'])
    def test_random_run(self, node):
        agents = [ppg.agents.RandomAgent()] * node.players
        while not node.is_game_over():
            node = node.get_next(agents[node.turn].get_move(node))
        assert True
