"""Gamestate and move class for the game of checkers.

The version of checkers implemented is English draughts:
https://en.wikipedia.org/wiki/English_draughts.

Checkers notation:

Black (first move)
|  | 1|  | 2|  | 3|  | 4|
| 5|  | 6|  | 7|  | 8|  |
|  | 9|  |10|  |11|  |12|
|13|  |14|  |15|  |16|  |
|  |17|  |18|  |19|  |20|
|21|  |22|  |23|  |24|  |
|  |25|  |26|  |27|  |28|
|29|  |30|  |31|  |32|  |
Red
"""

import numpy as np
import random
from pyboardgames.games.template import GamestateTemplate, MoveTemplate


class CheckersMove(MoveTemplate):
    """Wrapper for a checkers move.

    Moves are fed in as a tuple of tuples. Each inner tuple are
    coordinates corresponding to a square on the board; the first
    coordinate pair is the position of the piece to move, while later
    coordinate pairs are positions moved to.
    """

    def __init__(self, squares):
        """Initialize move wrapper.

        Args:
            squares: A tuple of coordinates, each cooresponding to a
                square on the checkers board.
        """
        self._squares = squares
        self._jumps = []
        self._dirs = []

    def __getitem__(self, key):
        """Allow direct access to squares tuple."""
        return self._squares[key]

    def __len__(self):
        """Length of move is number of squares involved."""
        return len(self._squares)

    def _notation(self, key):
        """Output selected square in standard notation."""
        return (1 + (8*self._squares[key][0] + self._squares[key][1]) // 2)

    def __str__(self):
        """Write the move as a string using the squares coordinates."""
        move_string = str(self._notation(0))
        for ind in range(1, len(self._squares)):
            move_string += "-" + str(self._notation(ind))
        return move_string

    @property
    def jumps(self):
        """Determine which squares are jumped, if any.

        May have unexpected results on invalid moves.
        """
        if not self._jumps:
            for start, end in zip(self._squares, self._squares[1:]):
                diff = (end[0] - start[0], end[1] - start[1])
                if diff[0] in (-2, 2) and diff[1] in (-2, 2):
                    self._jumps.append((start[0] + diff[0] // 2,
                                        start[1] + diff[1] // 2))
        return self._jumps

    @property
    def dirs(self):
        """Determine directions of moves."""
        if not self._dirs:
            for start, end in zip(self._squares, self._squares[1:]):
                diff = (end[0] - start[0], end[1] - start[1])
                self._dirs.append((1 if diff[0] > 0 else -1,
                                   1 if diff[1] > 0 else -1))
        return self._dirs


class CheckersGamestate(GamestateTemplate):
    """Instances represent the current state of a game of checkers.

    Contains all methods and properties to describe, set, and update
    the checkers gamestate.
    """

    TEAM_PIECES = [(1, 2), (-1, -2)]

    PIECE_DIRS = {1:  ((1, -1), (1, 1)),
                  -1: ((-1, -1), (-1, 1)),
                  2:  ((-1, -1), (-1, 1), (1, -1), (1, 1)),
                  -2: ((-1, -1), (-1, 1), (1, -1), (1, 1))}

    PIECE_TEAMS = {1: 0, 2: 0, -1: 1, -2: 1}

    COMPACT = {(0, 1): 0, (0, 3): 1, (0, 5): 2, (0, 7): 3,
               (1, 0): 4, (1, 2): 5, (1, 4): 6, (1, 6): 7,
               (2, 1): 8, (2, 3): 9, (2, 5): 10, (2, 7): 11,
               (3, 0): 12, (3, 2): 13, (3, 4): 14, (3, 6): 15,
               (4, 1): 16, (4, 3): 17, (4, 5): 18, (4, 7): 19,
               (5, 0): 20, (5, 2): 21, (5, 4): 22, (5, 6): 23,
               (6, 1): 24, (6, 3): 25, (6, 5): 26, (6, 7): 27,
               (7, 0): 28, (7, 2): 29, (7, 4): 30, (7, 6): 31}

    players = 2
    upper = 569988000.0
    lower = -569988000.0
    upper_sum = 0  # Zero sum game

    hash_length = 32

    def __init__(self,
                 board=None,
                 turn=0,
                 plys=0,
                 plys_since_cap=0,
                 hash_value=None,
                 hash_key=None):
        """Initialize the beginning of a game of checkers.

        Args:
            board: An 8x8 numpy array representing the game board. If no
                argument or None is passed, the board is initialized to
                the starting board.
            turn: An integer 0 or 1 noting if its black or red turn,
                respectively. Default value 0.
            plys: An integer tracking the number of plys (half-turns)
                taken in this game.
            plys_since_cap: An integer tracking the number of plys since
                the last capture. Used to implement the 40 turn draw
                rule.
        """
        if board is None:
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
        self._valid_moves = []
        self._winner = None
        self._score = None
        self.plys = plys
        self.plys_since_cap = plys_since_cap

        if hash_key is None:
            self.hash_key = [{piece: random.getrandbits(self.hash_length)
                              for piece in (-2, -1, 1, 2)}
                             for _ in range(32)]
        else:
            self.hash_key = hash_key
        if hash_value is None:
            self.hash_board()
        else:
            self.hash_value = hash_value

    @property
    def turn(self):
        """Get turn attribute.

        Returns:
            0: Black's turn
            1: Red's turn
        """
        return self._turn

    @turn.setter
    def turn(self, new_turn):
        """Set turn attribute and reset valid moves attribute.

        Turn attribute should not be set directly, but can be useful
        for debug and testing. In this case, valid_moves, score, and
        winner should be recalculated.
        """
        if new_turn != self._turn:
            self._turn = new_turn
            self._valid_moves = []
            self._winner = None
            self._score = None

    @property
    def turn_count(self):
        """A ply is a half turn.

        Returns:
            An integer corresponding to turns since the beginning of the
            game. Starts at 1, and increases after two plies.
        """
        return (self.plys // 2) + 1

    @property
    def score(self):
        """Score the current position.

        Returns: A tuple of 9-digit floats. The first entry is score
            for black, the second for red. From left to right, the
            digits of the score encode:
            1-2: Measures piece count and value for each team.
                +5 for turn player king, -5 for opponent king.
                +3 for turn player man, -3 for opponent man.
            3-4: Measures how close pieces are to becoming kings.
                For turn player, points are awarded according to how
                many rows each man is away from the end row. The
                negative of the same is awarded to the opponent.
            5-6: Measure of how many pieces are left on the board. If
                turn player is ahead according to the other heuristics,
                pieces left on the board are a detriment and are
                subtracted from the score; if the turn player is losing,
                pieces are instead added to the score. This encourages
                trading while ahead.
            7-9: Measures how well-placed kings are. Encourages
                centering kings. Both row and column are scored
                according to the equation -x(x-7), which is 0 on the
                edges and maximal towards the center.
        """
        if self._score is None:
            if self.winner == 0:
                return (float('inf'), float('-inf'))
            elif self.winner == 1:
                return (float('-inf'), float('inf'))
            elif self.winner == -1:
                return (0.0, 0.0)
            else:
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

    def jumps(self, square, piece):
        """Determine where a piece can jump to, if at all.

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
                    and step_2[1] in range(8)):
                if (self.board[step_1] in
                        self.TEAM_PIECES[-self.PIECE_TEAMS[piece]+1]
                        and self.board[step_2] == 0):
                    return_list[step_2] = step_1
            else:
                continue
        return return_list

    def jump_tree(self, square, piece, capt):
        """Find all jump moves from a given square and piece.

        Args:
            square: The square to analyze jumps from.
            piece: The piece on the square (note the piece may not be
                there on the board.)
            capt: A list of pieces that have previously been
                captured in the recursion. When initializing, use
                an empty list.

        Returns:
            A list contiaining tuples. Each tuple is a chain of jumps
            originating from the square input. The tuples themselves
            contain tuples representing squares that the chain lands on.
            These chains have all squares except the starting point.
        """
        return_list = []
        jump_dict = self.jumps(square, piece)
        for end, jump in jump_dict.items():
            if jump not in capt:
                jump_list = self.jump_tree(end, piece, capt + [jump])
                if not jump_list:
                    return_list += [(end,)]
                else:
                    return_list += [(end,) + tup for tup in jump_list]
        return return_list

    @property
    def valid_moves(self):
        """Return a list of all valid moves in this state.

        Returns:
            List of CheckerMove instances that constitute all valid
            moves for the current turn holder in this state.
        """
        if not self._valid_moves:
            # Captures
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece in self.TEAM_PIECES[self.turn]:
                        self.board[row][col] = 0
                        jump_list = self.jump_tree((row, col), piece, [])
                        self._valid_moves += [CheckersMove(((row, col),) + tup)
                                              for tup in jump_list]
                        self.board[row][col] = piece

            # Simple moves
            if not self._valid_moves:
                for row in range(8):
                    for col in range(8):
                        piece = self.board[row][col]
                        if piece in self.TEAM_PIECES[self.turn]:
                            for d in self.PIECE_DIRS[piece]:
                                if (row + d[0] in range(8)
                                        and col + d[1] in range(8)
                                        and self.board[row+d[0]][col+d[1]]
                                        == 0):
                                    move = CheckersMove(((row, col),
                                                         (row+d[0], col+d[1])))
                                    self._valid_moves.append(move)

        return self._valid_moves

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
