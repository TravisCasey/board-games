"""Gamestate and move class for the game of checkers.

The version of checkers implemented is English draughts:
https://en.wikipedia.org/wiki/English_draughts.
"""

import numpy as np
from pyboardgames.games.template import GamestateTemplate, MoveTemplate

class CheckersGamestate(GamestateTemplate):
    """Instances represent the current state of a game of checkers.
    
    Contains all methods and properties to describe, set, and update
    the checkers gamestate.
    """

    def __init__(self):
        """Initializes the beginning of a game of checkers."""

        self.board = np.asarray(
            [[0,  1,  0,  1,  0,  1,  0,  1],
             [1,  0,  1,  0,  1,  0,  1,  0],
             [0,  1,  0,  1,  0,  1,  0,  1],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [0,  0,  0,  0,  0,  0,  0,  0],
             [-1, 0, -1,  0, -1,  0, -1,  0],
             [0, -1,  0, -1,  0, -1,  0, -1],
             [-1, 0, -1,  0, -1,  0, -1,  0]]
        )
        self.turn = 1
        self._valid_moves = []
    
    def is_valid(self, move):
        """Checks if the given move is valid.
        
        Args:
            move: CheckersMove instance
            
        Returns:
            True: move is valid.
            False: otherwise.
        
        Raises:
            TypeError: move is not a CheckersMove instance.
        """
        pass
    
    def update(self, move):
        """Updates the gamestate according to the provided move.
        
        Args:
            move: CheckersMove instance.
        """

        pass



