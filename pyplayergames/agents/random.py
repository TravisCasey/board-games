"""
Agent class whose instances select moves randomly.
"""

import random
import pyplayergames as ppg


class RandomAgent(ppg.AgentType):
    """
    Agent choosing uniformly randomly from among valid moves.

    Parameters
    ----------
    name : str, optional

    Attributes
    ----------
    name : str
    """

    def __init__(self, **kwargs) -> None:

        self.name: str
        if 'name' in kwargs and isinstance(kwargs['name'], str):
            self.name = kwargs['name']
        else:
            self.name = 'Random Player'

    def reset(self) -> None:
        """
        Agent has no persistent attributes to reset.
        """

    def get_move(self, gamestate: ppg.GamestateType) -> ppg.MoveType:
        """Choose randomly from all valid moves.

        This method does not handle the IndexError thrown should the
        `get_moves` list be empty.

        Parameters
        ----------
        gamestate : GamestateType
            The `Gamestate` from which to choose a move.

        Returns
        -------
        move : MoveType
        """

        return random.choice(gamestate.get_moves())
