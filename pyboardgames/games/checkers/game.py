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

    def __init__(self, board=None, turn=1, plys=0, plys_since_cap=0):
        """Initializes the beginning of a game of checkers.

        Args:
            board: An 8x8 numpy array representing the game board. If no
                argument or None is passed, the board is initialized to
                the starting board.
            turn: An integer 1 or -1 noting if its team 1 or team 2
                turn, respectively. Default value 1.
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
        self.plys = plys
        self.plys_since_cap = plys_since_cap

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, new_turn):
        """Turn variable should not be set directly, but can be useful
        for debug and testing. In this case, valid_moves should be
        recalculated.
        """

        if new_turn != self._turn:
            self._turn = new_turn
            self._valid_moves = []

    @property
    def turn_count(self):
        """A ply is a half turn."""
        return (self.plys // 2) + 1

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
        # FIXME: is this method necessary

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
            capt = [jump_dict[move[1]]]
            # Temporarily remove starting piece from the board as it is
            # a valid square for the piece to land on after a series of
            # jumps.
            self.board[move[0]] = 0

            for start, end in zip(move[1:], move[2:]):
                jump_dict = self.jumps(start, piece)
                if end not in jump_dict:
                    self.board[move[0]] = piece
                    return False
                elif jump_dict[end] in capt:
                    self.board[move[0]] = piece
                    return False
                else:
                    capt.append(jump_dict[end])

            jump_dict = self.jumps(move[-1], piece)
            for square in jump_dict.values():
                if square not in capt:
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

    def jump_tree(self, square, piece, capt):
        """Finds all jump moves from a given square and piece.

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
        """Returns a list of all valid moves in this state.

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
        """Updates the gamestate according to the provided move.

        Note this method does not check that the move is valid; it is
        assumed that the move is sourced from the valid_moves list.

        Args:
            move: CheckersMove instance.

        Returns:
            A new CheckersGamestate instance that reflects the changes
            from the given move.
        """

        next_state = CheckersGamestate(board=np.copy(self.board),
                                       turn=-self.turn,
                                       plys=self.plys+1,
                                       plys_since_cap=self.plys_since_cap+1)

        piece = next_state.board[move[0]]
        next_state.board[move[0]] = 0

        # Remove captured pieces, if applicable.
        for start, end in zip(move[:], move[1:]):
            diff = (end[0] - start[0], end[1] - start[1])
            if diff[0] in (-2, 2) and diff[1] in (-2, 2):
                cap_square = (start[0] + diff[0]//2, start[1] + diff[1]//2)
                next_state.board[cap_square] = 0
                next_state.plys_since_cap = 0

        # Check if piece becomes a king.
        if self.turn == 1 and move[-1][0] == 7:
            next_state.board[move[-1]] = 2
        elif self.turn == -1 and move[-1][0] == 0:
            next_state.board[move[-1]] = -2
        else:
            next_state.board[move[-1]] = piece

        return next_state

    def is_game_over(self):
        pass

    @property
    def winner(self):
        return self._winner
