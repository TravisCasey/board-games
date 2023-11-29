"""
Functional testing for pyplayergames\\games\\checkers
"""
# pylint: disable=C0115, C0116, C0413, W0212, W0104

# Temp code
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

import pyplayergames as ppg

def test_random_run():
    runs = 10
    agent_1 = ppg.agents.RandomAgent(name='Random 1')
    agent_2 = ppg.agents.RandomAgent(name='Random 2')
    openings = (
        'PAYG',
        'TwoMove',
        'ThreeMove',
        'ElevenMan',
        'ElevenManTwoMove'
    )
    checkers_match = ppg.checkers.Match()
    for opening in openings:
        result = checkers_match.run(
            (agent_1, agent_2),
            count=runs,
            opening=opening
        )
        assert result[0] != runs
        assert result[1] != runs
