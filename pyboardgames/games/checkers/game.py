"""Gamestate and move class for the game of checkers.

The version of checkers implemented is English draughts:
https://en.wikipedia.org/wiki/English_draughts.
"""

import numpy as np
from pyboardgames.games.template import GamestateTemplate, MoveTemplate


class CheckersMove(MoveTemplate):
    """Wrapper for a checkers move.

    Moves are fed in as a tuple of tuples. Each inner tuple are
    coordinates corresponding to a square on the board; the first
    coordinate pair is the position of the piece to move, while later
    coordinate pairs are positions moved to.
    """

    def __init__(self, squares):
        """Initializes move wrapper.

        Args:
            squares: A tuple of coordinates, each cooresponding to a
                square on the checkers board.

        Raises:
            TypeError: If the squares input is not a tuple of tuples.
            ValueError: If the coordinate tuples are not of length two,
                or if their values exceed that of the sizes of the
                board; they should be 0 to 7.
        """

        if type(squares) is not tuple:
            raise TypeError('Expected squares input as a tuple.')
        if len(squares) < 2:
            raise ValueError('Requires at least two squares.')
        for square in squares:
            if type(square) is not tuple:
                raise TypeError('Board coordinates should be a tuple.')
            if len(square) != 2:
                raise ValueError('Squares should be a tuple of length two.')
            if square[0] not in range(8) or square[1] not in range(8):
                raise ValueError('Rows and columns should be in 0 to 7.')

        self._squares = squares

    def __getitem__(self, key):
        return self._squares[key]

    def __len__(self):
        return len(self._squares)


class CheckersGamestate(GamestateTemplate):
    """Instances represent the current state of a game of checkers.

    Contains all methods and properties to describe, set, and update
    the checkers gamestate.
    """

    TEAM_PIECES = {1:  (1, 2),
                   -1: (-1, -2)}

    PIECE_DIRS = {1:  ((1, -1), (1, 1)),
                  -1: ((-1, -1), (-1, 1)),
                  2:  ((-1, -1), (-1, 1), (1, -1), (1, 1)),
                  -2: ((-1, -1), (-1, 1), (1, -1), (1, 1))}

    PIECE_TEAMS = {1: 1, 2: 1, 0: 0, -1: -1, -2: -1}

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
        self._winner = None

    def jumps(self, square, piece):
        """Determines where a piece can jump to, if at all.

        Args:
            square: A tuple indicating the square of the piece to check.
            piece: Which piece is (or would be) on the given square.

        Returns:
            A dictionary where the keys are valid squares to jump to
            and the corresponding entries are the squares jumped over.
        """

        steps = [((square[0] + d[0], square[1] + d[1]),
                  (square[0] + 2*d[0], square[1] + 2*d[1]))
                 for d in self.PIECE_DIRS[piece]]

        return_list = {}
        for step_1, step_2 in steps:
            if (step_1[0] in range(8)
                    and step_1[1] in range(8)
                    and step_2[0] in range(8)
                    and step_1[1] in range(8)):
                if (self.board[step_1] in
                        self.TEAM_PIECES[-self.PIECE_TEAMS[piece]]
                        and self.board[step_2] == 0):
                    return_list[step_2] = step_1
            else:
                continue
        return return_list

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

        # Handles moves that are jumps.
        jump_dict = self.jumps(move[0], piece)
        if move[1] in jump_dict:
            # List tracks squares pieces are captured on to avoid
            # loops, as pieces are not actually removed from the board.
            captured = [jump_dict[move[1]]]
            # Temporarily remove starting piece from the board as it is
            # a valid square for the piece to land on after a series of
            # jumps.
            self.board[move[0]] = 0

            for start, end in zip(move[1:], move[2:]):
                jump_dict = self.jumps(start, piece)
                if end not in jump_dict:
                    self.board[move[0]] = piece
                    return False
                elif jump_dict[end] in captured:
                    self.board[move[0]] = piece
                    return False
                else:
                    captured.append(jump_dict[end])

            jump_dict = self.jumps(move[-1], piece)
            for square in jump_dict.values():
                if square not in captured:
                    self.board[move[0]] = piece
                    return False
            self.board[move[0]] = piece

        # Handles simple moves.
        elif (len(move) == 2
              and self.board[move[1]] == 0
              and (move[1][0] - move[0][0], move[1][1] - move[0][1])
              in self.PIECE_DIRS[piece]):
            # Test if any other pieces can jump
            for row in range(8):
                for col in range(8):
                    test_piece = self.board[row][col]
                    if test_piece in self.TEAM_PIECES[self.turn]:
                        if self.jumps((row, col), test_piece):
                            return False

        # Any other type of move is invalid.
        else:
            return False

        return True

    @property
    def valid_moves(self):
        return self._valid_moves

    def update(self, move):
        """Updates the gamestate according to the provided move.

        Args:
            move: CheckersMove instance.
        """

    def is_game_over(self):
        pass

    @property
    def winner(self):
        return self._winner

    def copy(self):
        pass
