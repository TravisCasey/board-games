"""Handles imports for the test package."""

import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

from pyplayergames.games.checkers import game
from pyplayergames.games.checkers import gui
from pyplayergames.agents.random import RandomAgent
from pyplayergames.agents.minimax import (IDDFSAgent,
                                          MaxnAgent,
                                          ParanoidAgent)
from pyplayergames.agents.montecarlo import MCTSAgent
