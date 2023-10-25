"""
Checkers game classes.
=====================

This module contains the move class and gamestate class for the game of
checkers The version of checkers implemented is American Checkers, as
maintained by the American Checkers Federation.

Checkers notation and orientation:

::

    Black (first move)

        0  1  2  3  4  5  6  7

    0  |  | 1|  | 2|  | 3|  | 4|
    1  | 5|  | 6|  | 7|  | 8|  |
    2  |  | 9|  |10|  |11|  |12|
    3  |13|  |14|  |15|  |16|  |
    4  |  |17|  |18|  |19|  |20|
    5  |21|  |22|  |23|  |24|  |
    6  |  |25|  |26|  |27|  |28|
    7  |29|  |30|  |31|  |32|  |

    Red
"""

import random
import numpy as np
import pyplayergames as ppg


def coord_conv(square):
    """
    Convert between board coordinates and standard checkers notation.
    """
    return (8 * square[0] + square[1])//2 + 1


class Move(ppg.MoveTemplate):
    """
    Checkers move class.

    Moves are encoded as a start tuple and a direction tuple.

    Parameters
    ----------
    start : tuple of int
        Tuple (row, column) indicating the square on the board the move
        starts from
    d : tuple of int
        Tuple (row dir, column dir) indicates the direction of the move.
        Entries are 1 or -1 to indicate if row/column will increase or
        decrease.

    Notes
    -----
    Each instance is not necessarily a complete turn; with multiple
    jumps, multiple Move instances are required to represent the turn.

    While this class does not store whether a move is a simple move,
    single jump, or multiple jump, there is no ambiguity when paired
    with a checkers Gamestate instance.

    A given Move instance is not necesarily valid; validity of a move
    makes sense only when paired with a checkers Gamestate instance.
    """

    def __init__(self, start, d):
        self.start = start
        self.d = d

    def __str__(self):
        """
        Express the move in a readable format.

        Returns
        -------
        str
            Standard checkers notation for the start square and
            the square in the direction of d separated by a dash. As the
            move may be a jump, the second number may be the square of
            the piece captured rather than where the piece lands.
        """
        end = (self.start[0] + self.d[0], self.start[1] + self.d[1])
        return (str(ppg.checkers.coord_conv(self.start))
                + '-' + str(ppg.checkers.coord_conv(end)))


class Gamestate(ppg.GamestateTemplate):
    """
    Checkers Gamestate class.

    Parameters
    ----------
    board: NumPy array or NoneType, optional
        An 8x8 array representing the current checkers board. Default
        value is None, in which case the board will be set to the
        beginning game position.
    turn: {0, 1}, optional
        Sets the turn of the game. Value of 0 indicates it is black's
        turn (who moves first) while 1 indicates red's turn.
    last_piece: tuple of int or NoneType, optional
        Indicates the square of the last piece moved as part of a
        multiple move. Value of None indicates no multiple move.
    plys: int, optional
        Number of plys (half-turns) so far in the game. A single move
        instance may not correlate to a single ply due to multiple
        jump moves.
    plys_since_cap: int, optional
        Number of plys since the last piece was captured. At 80 plys
        (40 turns) since the last capture by either player, the game is
        declared a draw.

    Attributes
    ----------
    board: NumPy array
    turn: {0, 1}
    plys: int
    plys_since_cap: int
    valid_moves: list of Move instances
    score: tuple of float
    reward: tuple of float
    winner: int
    hash_value: int

    Other Parameters
    ----------------
    hash_key: list of dict of ints or NoneType, optional
        See hash_update method for documentation of hashing scheme.
        Value of None indicates the hash key should be generated.
    hash_value: int or NoneType, optional
        Value of None indicates the hash value should be calculated
        from the board.
    """

    players = 2
    lower = -569988000.0
    upper_sum = 0

    _hash_length = 32

    # Constants useful for calculations.
    _TEAM_PIECES = [(1, 2), (-1, -2)]

    _PIECE_DIRS = {1:  ((1, -1), (1, 1)),
                   -1: ((-1, -1), (-1, 1)),
                   2:  ((-1, -1), (-1, 1), (1, -1), (1, 1)),
                   -2: ((-1, -1), (-1, 1), (1, -1), (1, 1))}

    _PIECE_TEAMS = {1: 0, 2: 0, -1: 1, -2: 1}

    def __init__(self,
                 board=None,
                 turn=0,
                 last_piece=None,
                 plys=0,
                 plys_since_cap=0,
                 hash_value=None,
                 hash_key=None):
        if board is None:
            # Board at beginning of checkers game.
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
        else:
            self.board = board
        self._turn = turn
        self._last_piece = last_piece
        self.plys = plys
        self.plys_since_cap = plys_since_cap

        # Calculated as needed.
        self._valid_moves = []
        self._score = None
        self._reward = None
        self._winner = None

        # Generated hash key and hash value if none are given.
        if hash_key is None:
            self._hash_key = [{piece: random.getrandbits(self._hash_length)
                               for piece in (-2, -1, 1, 2)}
                              for _ in range(32)]
        else:
            self._hash_key = hash_key
        if hash_value is None:
            self.hash_board()
        else:
            self.hash_value = hash_value

    @property
    def turn(self):
        """
        Get turn attribute.

        Returns
        -------
            turn: int
                0 for Black's turn, 1 for Red's turn.
        """
        return self._turn

    @turn.setter
    def turn(self, new_turn):
        """
        Set turn attribute and reset turn dependent attributes.

        Turn attribute should not be set directly, but can be useful
        for testing.
        """
        if new_turn != self._turn:
            self._turn = new_turn
            self._last_piece = None
            self._valid_moves = []
            self._score = None
            self._reward = None
            self._winner = None

    @property
    def score(self):
        """
        Score the current position heuristically.

        The score is calculated for black, then negated for red.
        Score is a 9 digit float; from left to right, the digits encode:
            -1-2: Piece evaluation.
            -3-4: Encourages advancing men down the board.
            -5-6: Encourages trading while ahead.
            -7-9: Encourages centering kings.

        Returns
        -------
        score: tuple of floats
            A tuple of two 9 digit floats as described above. First
            entry is for black, the second for red.
        """
        if self._score is None:
            if self.winner == 0:
                return (float('inf'), float('-inf'))
            if self.winner == 1:
                return (float('-inf'), float('inf'))
            if self.winner == -1:
                return (0.0, 0.0)
            black_score = 0.0
            piece_count = 0
            for row in range(8):
                for col in range(8):
                    match self.board[row][col]:
                        case 1:
                            black_score += 30000000
                            black_score += row * 100000
                            piece_count += 1
                        case 2:
                            black_score += 50000000
                            black_score += row * (7 - row)
                            black_score += col * (7 - col)
                            piece_count += 1
                        case -1:
                            black_score -= 30000000
                            black_score -= (7 - row) * 100000
                            piece_count += 1
                        case -2:
                            black_score -= 50000000
                            black_score -= row * (7 - row)
                            black_score -= col * (7 - col)
                            piece_count += 1
            if black_score > 0:
                black_score -= piece_count * 1000
            elif black_score < 0:
                black_score += piece_count * 1000
            self._score = (black_score, -black_score)
        return self._score

    def piece_moves(self, square):
        move_list = []
        capt_list = []
        if piece := self.board[square] in self._TEAM_PIECES[self.turn]:
            for d in self._PIECE_DIRS[piece]:
                try:
                    square_1 = [square[0] + d[0], square[1] + d[1]]
                    if self.board[square_1] == 0:
                        move_list.append(ppg.checkers.Move(square, d))
                        continue
                    square_2 = [square_1[0] + d[0], square_1[1] + d[1]]
                    if (self.board[square_2] == 0 and
                        (self.board[square_1]
                             not in self._TEAM_PIECES[self.turn])):
                        capt_list.append(ppg.checkers.Move(square, d))
                        continue
                except IndexError:
                    continue
        return move_list, capt_list




    @property
    def valid_moves(self):
        if self._last_piece is not None:
            return self.piece_moves(self._last_piece)[1]
        move_list = []
        capt_list = []
        for row in range(8):
            for col in range(8):
                new_moves, new_capts = self.piece_moves((row, col))
                move_list += new_moves
                capt_list += new_capts
        if not capt_list:
            return move_list
        return capt_list

    def get_next(self, move):
        """Update the gamestate according to the provided move.

        Note this method does not check that the move is valid; it is
        assumed that the move is sourced from the valid_moves list.

        Args:
            move: CheckersMove instance.

        Returns:
            A new CheckersGamestate instance that reflects the changes
            from the given move.
        """
        next_state = CheckersGamestate(board=np.copy(self.board),
                                       turn=-self.turn+1,
                                       plys=self.plys+1,
                                       plys_since_cap=self.plys_since_cap+1,
                                       hash_value=self.hash_value,
                                       hash_key=self.hash_key)

        next_state.hash_update(move[0])
        piece = next_state.board[move[0]]
        next_state.board[move[0]] = 0

        # Remove captured pieces, if applicable.
        if move.jumps:
            next_state.plys_since_cap = 0
            for square in move.jumps:
                next_state.hash_update(square)
                next_state.board[square] = 0

        # Check if piece becomes a king.
        if self.turn == 0 and move[-1][0] == 7:
            next_state.board[move[-1]] = 2
        elif self.turn == 1 and move[-1][0] == 0:
            next_state.board[move[-1]] = -2
        else:
            next_state.board[move[-1]] = piece
        next_state.hash_update(move[-1])

        return next_state

    @property
    def winner(self):
        """Determine the winner of the game, if any.

        Returns:
            0: Black wins
            1: Red wins
            -1: Draw (40 turn since last capture.)
            None: Game is not over yet - no winner.
        """
        if self._winner is None:
            if not self.valid_moves:
                self._winner = -self.turn+1
            elif self.plys_since_cap >= 80:
                self._winner = -1
        return self._winner

    def is_game_over(self):
        """Determine if there is a winner of the game."""
        return self.winner is not None

    @property
    def reward(self):
        """Return a tuple of reward based on outcome of the game."""
        if self.winner == 0:
            return (1.0, 0.0)
        elif self.winner == 1:
            return (0.0, 1.0)
        elif self.winner == -1:
            return (0.5, 0.5)
        else:
            raise ValueError

    def hash_board(self):
        """Calculate hash value of current board state."""
        self.hash_value = 0
        for square in self.COMPACT.keys():
            self.hash_update(square)

    def hash_update(self, square):
        """Update hash value with piece at given square.

        Should be called before a piece is removed from the square or
        after a piece is added to the square.

        Args:
            square: A tuple indicating a square of the board.
        """
        piece = self.board[square]
        if piece != 0:
            self.hash_value ^= self.hash_key[self.COMPACT[square]][piece]
