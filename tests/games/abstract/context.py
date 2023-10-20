"""Handles imports for the test package."""

import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

from pyplayergames.games.abstract import game
from pyplayergames.agents.random import RandomAgent
