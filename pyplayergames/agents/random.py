"""A simple agent that selects move uniformly randomly."""

from pyplayergames.agents.template import AgentTemplate
import random


class RandomAgent(AgentTemplate):
    """Agent chooses uniformly randomly from valid moves."""

    def __init__(self, **kwargs):
        """Initialize the agent's attributes.

        Args:
            name: A keyword arg designating a name for the player.
        """
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'Random Player'

    def reset(self):
        """Fulfills agent template requirement."""
        pass

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
