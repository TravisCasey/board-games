"""
Checkers
========

This module contains the logic and implementation for the game of
checkers. The version of checkers implemented is American Checkers.

Notes
-----
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

from __future__ import annotations
import random
import numpy as np
from numpy.typing import NDArray
import pyplayergames as ppg


def coord_to_num(square: tuple[int, int]) -> int:
    """
    Convert between board coordinates and standard checkers notation.

    Parameters
    ----------
    square: tuple of int
        (row, column) notation indexing the `board` attribute.

    Returns
    -------
    int
        Standard checkers notation.
    """

    return (8 * square[0] + square[1])//2 + 1

def coord_sum(square: tuple[int, int], d: tuple[int, int]) -> tuple[int, int]:
    """
    Calculate next square in direction provided.
    """

    return (square[0] + d[0], square[1] + d[1])


class Move:
    """
    Checkers `Move` class.

    Moves are encoded as a start tuple and a direction tuple.

    Parameters
    ----------
    start : tuple of int
        Square on the board the move starts from.
    d : tuple of int
        Direction of the move. Entries are 1 or -1 to indicate if
        row/column will increase or decrease.
    capt : bool
        True if the move is a capture, False for a simple move.

    Notes
    -----
    Each instance is not necessarily a complete turn; with multiple
    jumps, multiple `Move` instances are required to represent the turn.
    """

    def __init__(
        self,
        start: tuple[int, int],
        d: tuple[int, int],
        capt: bool
        ) -> None:

        self.start = start
        self.d = d
        self.capt = capt

    def __str__(self) -> str:
        """
        Express the move in a readable format.

        Returns
        -------
        str
            Standard checkers notation for `start` attribute and
            the square in the direction of `d` separated by - for a
            simple move or x for a capture.
        """

        start_num = ppg.checkers.coord_to_num(self.start)
        end = ppg.checkers.coord_sum(self.start, self.d)
        end_num = ppg.checkers.coord_to_num(end)
        if self.capt:
            return f'{start_num}x{end_num}'
        return f'{start_num}-{end_num}'


class Gamestate:
    """
    Checkers `Gamestate` class.

    Parameters
    ----------
    parent : Gamestate instance, optional
        The `Gamestate` prior to this instance. The new instance is
        initialized by updating this `Gamestate` with the `Move`
        parameter. If set to None, the new `Gamestate` instance will
        instead reference the other parameters for state information.
    move : Move instance, optional
        The move immediately prior to the gamestate. When the gamestate
        is initialized, the board is updated to reflect this move. Value
        of None applies no update.
    board : NumPy array, optional
        An 8x8 array representing the current checkers board. Default
        value is None, in which case the board will be set to the
        beginning game position.
    turn : {0, 1}, optional
        Sets the turn of the game. Default value of 0 indicates it is
        black's turn (who moves first) while 1 indicates red's turn.
    plys_to_draw : int, optional
        Number of plys (half-turns) since the last piece was captured or
        man was advanced. A single move instance may not correlate to a
        single ply due to multiple jump moves. At 80 plys (40 turns)
        since the last capture or man advancement by either player, the
        game is declared a draw.
    hash_value : int, optional
        Value of None indicates the hash value should be calculated
        from the board.

    Attributes
    ----------
    parent : `Gamestate` instance, optional
    board : `numpy` array
    turn : {0, 1}
    plys_to_draw : int
    valid_moves : list of `Move` instances
    score : tuple of float
    reward : tuple of float
    winner : int
    hash_key : dict
    hash_count : dict

    """

    players = 2
    lower = -569987252.0
    upper_sum = 0.0

    _hash_length = 32

    # Constants useful for calculations.
    _TEAM_PIECES: list[tuple[int, int]] = [(1, 2), (-1, -2)]

    _PIECE_DIRS: dict[int, tuple[tuple[int, int], ...]] = {
        1:  ((1, -1), (1, 1)),
        -1: ((-1, -1), (-1, 1)),
        2:  ((-1, -1), (-1, 1), (1, -1), (1, 1)),
        -2: ((-1, -1), (-1, 1), (1, -1), (1, 1))
        }

    _PIECE_TEAMS: dict[int, int] = {1: 0, 2: 0, -1: 1, -2: 1}

    _SQUARES: tuple[tuple[int, int], ...] = (
        (0, 1), (0, 3), (0, 5), (0, 7),
        (1, 0), (1, 2), (1, 4), (1, 6),
        (2, 1), (2, 3), (2, 5), (2, 7),
        (3, 0), (3, 2), (3, 4), (3, 6),
        (4, 1), (4, 3), (4, 5), (4, 7),
        (5, 0), (5, 2), (5, 4), (5, 6),
        (6, 1), (6, 3), (6, 5), (6, 7),
        (7, 0), (7, 2), (7, 4), (7, 6)
        )

    def __init__(
        self,
        parent: ppg.checkers.Gamestate | None = None,
        move: ppg.checkers.Move | None = None,
        board: NDArray[np.int_] | None = None,
        turn: int = 0,
        plys_to_draw: int = 0,
        hash_value: int | None = None
        ) -> None:

        self.board: NDArray[np.int_]
        self._turn: int
        self.plys_to_draw: int
        self._valid_moves: list[ppg.checkers.Move] = []
        self.hash_key: dict[tuple[int, int], dict[int, int]]
        self._hash_value: int
        self.hash_count: dict[int, tuple[list[ppg.checkers.Gamestate],
                                         list[ppg.checkers.Gamestate]]]
        self._score: tuple[float, float] | None = None
        self._reward: tuple[float, float] | None = None
        self._winner: int | None = None

        if parent is not None:
            self.board = np.copy(parent.board)
            self._turn = parent.turn
            self.plys_to_draw = parent.plys_to_draw
            self.hash_key = parent.hash_key
            self._hash_value = hash(parent)
            self.hash_count = parent.hash_count
        else:
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
            self.plys_to_draw = plys_to_draw

            # Generate hash key and hash value if none are given.
            self.hash_key = {
                square: {
                    piece: random.getrandbits(self._hash_length)
                    for piece in (-2, -1, 1, 2)
                    }
                for square in self._SQUARES
                }
            if hash_value is None:
                self._hash_board()
            else:
                self._hash_value = hash_value

        # Set state according to provided move
        # Jump
        if move is not None and move.capt:
            self.plys_to_draw = 0
            piece = self.board[move.start]
            square_1 = ppg.checkers.coord_sum(move.start, move.d)
            square_2 = ppg.checkers.coord_sum(square_1, move.d)
            self._update_board(move.start, 0)
            self._update_board(square_1, 0)

            # Test for man becoming a king
            if piece in (1, -1) and square_2[0] in (0, 7):
                self._update_board(square_2, 2*piece)
                self._turn = -self.turn + 1

            # Test for a continuing jump move
            else:
                self._update_board(square_2, piece)
                move_list = self.piece_moves(square_2)
                if move_list[1]:
                    self._valid_moves = move_list[1]
                else:
                    self._turn = -self.turn + 1

            if self._turn == 0:
                self.hash_count = {self._hash_value: ([self], [])}
            else:
                self.hash_count = {self._hash_value: ([], [self])}

        # Simple move
        elif move is not None:
            self._turn = -self.turn + 1
            piece = self.board[move.start]

            square_1 = ppg.checkers.coord_sum(move.start, move.d)
            self._update_board(move.start, 0)

            # Test for man becoming a king
            if piece in (1, -1) and square_1[0] in (0, 7):
                self._update_board(square_1, 2*piece)
            else:
                self._update_board(square_1, piece)

            if piece in (1, -1):
                self.plys_to_draw = 0
                if self._turn == 0:
                    self.hash_count = {self._hash_value: ([self], [])}
                else:
                    self.hash_count = {self._hash_value: ([], [self])}
            else:
                self.plys_to_draw += 1
                self.hash_count.setdefault(
                    self._hash_value,
                    ([], [])
                    )[self._turn].append(self)
        else:
            if self._turn == 0:
                self.hash_count = {self._hash_value: ([self], [])}
            else:
                self.hash_count = {self._hash_value: ([], [self])}


    # Interface Methods

    def get_next(self, move: ppg.checkers.Move) -> ppg.checkers.Gamestate:
        """
        Generate the next `Gamestate` according to the provided move.

        Parameters
        ----------
        move : Move instance
            Assumed to be from `valid_moves` attribute.

        Returns
        -------
        Gamestate instance
            A new Gamestate instance that reflects the changes from the
            given move.
        """
        return ppg.checkers.Gamestate(parent=self, move=move)

    def is_game_over(self) -> bool:
        """
        Determine if the game is over.

        Returns
        -------
        bool
            True if the game is over, False otherwise.
        """
        return self.winner is not None

    def __hash__(self) -> int:
        return self._hash_value

    def piece_moves(
        self,
        square: tuple[int, int]
        ) -> tuple[list[ppg.checkers.Move], list[ppg.checkers.Move]]:
        """
        Generate possible `Move` instances from an individual square.

        Tests both simple moves and captures. `Move` instances generated
        are not necessarily valid; for example, no simple moves are
        valid if there are captures available.

        Parameters
        ----------
        square : tuple of int
            The square on the board to generate moves from.

        Returns
        -------
        move_list : list of Move instances
            List of simple moves.
        capt_list : list of Move instances
            List of captures.
        """

        move_list = []
        capt_list = []
        piece = self.board[square]
        if piece in self._TEAM_PIECES[self.turn]:
            for d in self._PIECE_DIRS[piece]:
                try:
                    square_1 = ppg.checkers.coord_sum(square, d)
                    if self.board[square_1] == 0:
                        move_list.append(ppg.checkers.Move(square, d, False))
                        continue
                    square_2 = ppg.checkers.coord_sum(square_1, d)
                    if (self.board[square_2] == 0
                        and (self.board[square_1]
                             not in self._TEAM_PIECES[self.turn])):
                        capt_list.append(ppg.checkers.Move(square, d, True))
                except IndexError:
                    continue
        return move_list, capt_list

    # Properties

    @property
    def turn(self) -> int:
        """
        Get turn attribute.

        Returns
        -------
        turn : {0, 1}
            0 for Black's turn, 1 for Red's turn.
        """

        return self._turn

    @turn.setter
    def turn(self, new_turn: int) -> None:
        """
        Set turn attribute and reset turn dependent attributes.

        Turn attribute should not be set directly, but can be useful
        for testing.
        """

        if new_turn != self._turn:
            self._turn = new_turn
            self._valid_moves = []
            self._score = None
            self._reward = None
            self._winner = None

    @property
    def valid_moves(self) -> list[ppg.checkers.Move]:
        """
        A list of all valid moves in the current state.
        """

        if not self._valid_moves:
            move_list = []
            capt_list = []
            for square in self._SQUARES:
                new_moves, new_capts = self.piece_moves(square)
                move_list += new_moves
                capt_list += new_capts

            # Simple moves are only valid if there are no captures.
            if not capt_list:
                self._valid_moves = move_list
            else:
                self._valid_moves = capt_list
        return self._valid_moves

    @valid_moves.setter
    def valid_moves(self, new_valid_moves: list[ppg.checkers.Move]) -> None:
        """
        Set the `valid_moves` attribute directly.

        No checks on validity are made. This functionality is inteded
        for setting the `valid_moves` attribute of a newly created
        `Gamestate` instance with an ongoing multiple jump.
        """

        self._valid_moves = new_valid_moves

    @property
    def winner(self) -> int | None:
        """
        Determine the winner of the game, if any.

        Black wins if Red has no valid moves on their turn and vice
        versa. A draw occurs when either 40 turns have passed since the
        last capture or advancement of a man, or the same position has
        occured 3 times in the game.

        Returns
        -------
        {0, 1, -1}, optional
            0 indicates Black wins. 1 indicates Red wins. -1 indicates a
            draw. None indicates the game is not over.
        """

        if self._winner is None:
            if not self.valid_moves:
                self._winner = -self.turn + 1
            elif self.plys_to_draw >= 80:
                self._winner = -1
            else:
                try:
                    match_list = self.hash_count[self._hash_value][self._turn]
                    if len(match_list) >= 3:
                        matches: int = 0
                        for gamestate in match_list[:-1]:
                            if np.array_equal(self.board, gamestate.board):
                                matches += 1
                        if matches >= 2:
                            self._winner = -1
                except KeyError:
                    pass
        return self._winner

    @property
    def reward(self) -> tuple[float, float]:
        """
        Return a player-based reward based on outcome of the game.

        Differs from the `score` attribute as the reward is only
        calculated at the end of the game.

        Returns
        -------
        tuple of float
            Players receive 1 point for a win and 0 for a loss. Each
            receive 0.5 for a draw.

        Raises
        ------
        AttributeError
            Exception is raised if this attribute is referenced before
            the end of the game.
        """

        if self.winner == 0:
            return (1.0, 0.0)
        if self.winner == 1:
            return (0.0, 1.0)
        if self.winner == -1:
            return (0.5, 0.5)
        raise AttributeError(
            'Reward attribute referenced before the game is over'
            )

    @property
    def score(self) -> tuple[float, float]:
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
        score : tuple of float
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
            centering_score = 0.0
            piece_count = 0
            for square in self._SQUARES:
                match self.board[square]:
                    case 1:
                        black_score += 30000000.0
                        black_score += square[0] * 100000.0
                        piece_count += 1
                    case 2:
                        black_score += 50000000.0
                        centering_score += square[0] * (7 - square[0])
                        centering_score += square[1] * (7 - square[1])
                        piece_count += 1
                    case -1:
                        black_score -= 30000000.0
                        black_score -= (7 - square[0]) * 100000.0
                        piece_count += 1
                    case -2:
                        black_score -= 50000000.0
                        centering_score -= square[0] * (7 - square[0])
                        centering_score -= square[1] * (7 - square[1])
                        piece_count += 1

            if black_score > 0.0:
                black_score -= piece_count * 1000.0
            elif black_score < 0.0:
                black_score += piece_count * 1000.0
            black_score += centering_score
            self._score = (black_score, -black_score)
        return self._score

    # Private Methods

    def _update_board(self, square: tuple[int, int], piece: int) -> None:
        """
        Updates and hashes the board.

        Parameters
        ----------
        square : tuple of int
            Square on board to update to new piece.
        piece : {-2, -1, 0, 1, 2}
            New piece to place on the square.
        """

        self._hash_update(square)
        self.board[square] = piece
        self._hash_update(square)

    def _hash_update(self, square: tuple[int, int]) -> None:
        """
        Update hash with piece at given square.

        Method should be called before a piece is removed from the
        square and after a piece is added to the square.
        See `_update_board` method.
        """

        piece = self.board[square]
        if piece != 0:
            self._hash_value ^= self.hash_key[square][piece]

    def _hash_board(self) -> None:
        """
        Calculate hash of current board state.

        Hashes are typically set iteratively when pieces are added and
        removed according to the `_hash_update` method. However, the hash
        can be calculated from scratch with this method.
        """

        self._hash_value = 0
        for square in self._SQUARES:
            self._hash_update(square)
