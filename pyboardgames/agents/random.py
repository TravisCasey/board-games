"""A simple agent that selects move uniformly randomly."""

from pyboardgames.agents.template import AgentTemplate
import random


class RandomAgent(AgentTemplate):
    """Agent chooses uniformly randomly from valid moves."""

    def __init__(self, name='Random Agent', time=0.0):
        """Initialize the agent's attributes."""
        self.name = name
        self.time = time

    def get_move(self, gamestate):
        """Choose randomly from all valid moves.

        Note this method does not handle the IndexError thrown by
        random.choice should the valid_moves list be empty.

        Args:
            gamestate: An instance of a Gamestate class

        Returns:
            An instance from the proper Move class corresponding to the
            given gamestate.
        """
        return random.choice(gamestate.valid_moves)
