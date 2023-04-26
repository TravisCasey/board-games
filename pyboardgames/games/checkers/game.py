"""Gamestate and move class for the game of checkers.

The version of checkers implemented is English draughts:
https://en.wikipedia.org/wiki/English_draughts.
"""

import numpy as np
from pyboardgames.games.template import GamestateTemplate, MoveTemplate

class CheckersMove(MoveTemplate):
    """Container for a checkers move.
    
    Moves are fed in as a tuple of tuples. Each inner tuple are
    coordinates corresponding to a square on the board; the first
    coordinate is the position of the piece to move, while later
    coordinates are positions moved to. 
    """

    def __init__(self, positions):
        self.positions = positions
        self._submoves = []

    def __getitem__(self, key):
        return self.positions[key]
    
    def __len__(self):
        return len(self.positions)

    @property
    def submoves(self):
        """Generates submoves when called unless already generated.

        Submoves of a full move are the original move broken into
        individual jumps (or simple moves if not a jump).

        Returns:
            A list of submoves.

        Example:
            Let self.positions = ((0, 1), (2, 3), (4, 5)). Then 
            self.submoves = [((0, 1), (2, 3)), ((2, 3), (4, 5))] 
        """
        if not self._submoves:
            for ind in range(len(self.positions) - 1):
                self._submoves.append(self.positions[ind:ind + 1])
        return self._submoves


class CheckersGamestate(GamestateTemplate):
    """Instances represent the current state of a game of checkers.
    
    Contains all methods and properties to describe, set, and update
    the checkers gamestate.
    """

    TEAM_PIECES = {1:  (1, 2),
                   -1: (-1, -2)}

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
        """

        # Check if there is a piece of the correct team at the first
        # position of the move.
        piece = self.board[move[0]]
        if piece not in self.TEAM_PIECES[self.turn]:
            return False
        
        

        return True

    def update(self, move):
        """Updates the gamestate according to the provided move.
        
        Args:
            move: CheckersMove instance.
        """
