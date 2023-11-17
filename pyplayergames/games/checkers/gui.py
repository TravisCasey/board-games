"""
Checkers GUI
============

This module contains the graphical interface for the checkers game. The
`GUI` class handles automatically played games as well as user input for
manually played games.

"""

from __future__ import annotations
from typing import Any
import os
import tkinter as tk

# FIXME: temporary import fix
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))

import pyplayergames as ppg


class GUI:
    """
    Graphical user interface for checkers.

    Written using the `tkinter` package. Displays checkerboard that
    accepts move input (on the turn of a manual player) and has a basic
    menu at the bottom.

    Attributes
    ----------
    window : Tk
    terminated_flag : bool
    restart_game_flag : bool
    restart_match_flag : bool

    Notes
    -----
    The GUI class does not generate moves or make calls to any agent
    instances. Outside calls to the `update_board_and_text` method are
    expected with new checkers `Gamestate` instances.

    Intended to be run by an instance of the checkers `Match` class

    """

    # Hex color codes
    _LIGHT_COL: str = '#FFBE7D'
    _DARK_COL: str = '#FF7F3F'
    _SEL_COL: str = '#00CCFF'
    _VALID_COL: str = '#00FFFF'
    _MENU_COL: str = '#B3B3B3'
    _TURN_COL: str = '#0088CC'

    # Space and sizing settings
    _SQUARE_PIX: int = 80
    _PIECE_PAD: int = 5
    _KING_PAD: int = 20
    _MENU_HEIGHT: int = 200

    # Button settings
    _button_options: dict[str, Any] = {
        'bg': 'yellow',
        'activebackground': 'yellow',
        'font': ('', 20),
        'width': 3,
        'height': 1,
        'border': 4
    }
    _button_padding: dict[str, Any] = {
        'padx': 0,
        'pady': 20
    }
    _text_font: tuple[str, int] = ('Helvetica', 18)

    def __init__(self) -> None:
        # Generate window
        self.window = tk.Tk()
        self.window.configure(bg=self._MENU_COL)
        self.window.geometry('640x840')
        self.window.title('Checkers')
        self.window.resizable(False, False)
        icon_path = os.path.join(os.path.dirname(__file__), './icon.png')
        self.window.iconphoto(
            False,
            tk.PhotoImage(file=icon_path)
        )
        # See the `_on_exit` method.
        self.window.protocol('WM_DELETE_WINDOW', self._on_exit)
        self.terminated_flag: bool = False

        # Attributes related to manual move input
        self._manual: bool = False
        self._moves: tuple[ppg.MoveType, ...] = ()
        self._valid: list[tuple[int, int]] = []
        self._selected: tuple[int, int] | None = None
        self._manual_move: ppg.MoveType | None = None

        # Draw board.
        self._board_ref: dict[int, tuple[int, int]] = {}
        self._piece_ref: dict[int, tuple[int, int]] = {}
        self._square_ref: dict[tuple[int, int], int] = {}
        self._board_c = tk.Canvas(
            self.window,
            width=8*self._SQUARE_PIX,
            height=8*self._SQUARE_PIX
        )
        self._board_c.pack()
        for row in range(8):
            for col in range(8):
                if row % 2 == col % 2:
                    color = self._LIGHT_COL
                else:
                    color = self._DARK_COL
                square_id = self._board_c.create_rectangle(
                    col*self._SQUARE_PIX,
                    row*self._SQUARE_PIX,
                    (col+1)*self._SQUARE_PIX,
                    (row+1)*self._SQUARE_PIX,
                    fill=color,
                    tags='square'
                )
                self._board_ref[square_id] = (row, col)
                self._square_ref[(row, col)] = square_id
        self._board_c.tag_bind('square', '<ButtonPress-1>', self._clicked)
        self._board_c.tag_bind('piece', '<ButtonPress-1>', self._clicked)

        # Buttons
        self._menu_frame = tk.Frame(
            self.window,
            width=8*self._SQUARE_PIX,
            height=self._MENU_HEIGHT,
            bg=self._MENU_COL
        )
        self._menu_frame.pack()
        self._menu_frame.columnconfigure(0, minsize=4*self._SQUARE_PIX)
        self._menu_frame.columnconfigure((2, 3), minsize=1.5*self._SQUARE_PIX)
        self._menu_frame.columnconfigure((1, 4), minsize=0.5*self._SQUARE_PIX)

        self._restart_game_button = tk.Button(
            self._menu_frame,
            text='\u23EE',
            command=self._restart_game,
            relief=tk.RAISED,
            **self._button_options
        )
        self._restart_game_button.grid(
            row=0, column=2, **self._button_padding
        )
        self.restart_game_flag: bool = False

        self._play_pause_button = tk.Button(
            self._menu_frame,
            text='\u23EF',
            command=self._play_pause,
            relief=tk.RAISED,
            **self._button_options
        )
        self._play_pause_button.grid(
            row=0, column=3, **self._button_padding
        )
        self.pause_flag: bool = False

        self.match_text = tk.StringVar(self._menu_frame, '')
        tk.Label(
            self._menu_frame,
            font=self._text_font,
            bg=self._MENU_COL,
            textvariable=self.match_text
        ).grid(
            row=0, column=0, columnspan=2, sticky='W', padx=40
        )

        self.player_1_text = tk.StringVar(self._menu_frame, '')
        self._player_1_label = tk.Label(
            self._menu_frame,
            font=self._text_font,
            bg=self._MENU_COL,
            textvariable=self.player_1_text
        )
        self._player_1_label.grid(
            row=1, column=0, columnspan=5, sticky='W', padx=40
        )

        self.player_2_text = tk.StringVar(self._menu_frame, '')
        self._player_2_label = tk.Label(
            self._menu_frame,
            font=self._text_font,
            bg=self._MENU_COL,
            textvariable=self.player_2_text
        )
        self._player_2_label.grid(
            row=2, column=0, columnspan=5, sticky='W', padx=40
        )

    # Interface

    def update_state(self, gamestate: ppg.checkers.Gamestate) -> None:
        """
        Updates the GUI to the new gamestate.

        Parameters
        ----------
        gamestate : checkers `Gamestate`
        matches_complete : int
        matches_total : int
        agent_name : str
        """

        # Remove pieces.
        self._board_c.delete('piece')
        self._piece_ref = {}

        # Draw new pieces back.
        for row in range(8):
            for col in range(8):
                match gamestate.board[row][col]:
                    case 1:
                        self._draw_piece(row, col, 0)
                    case 2:
                        self._draw_piece(row, col, 0, king=True)
                    case -1:
                        self._draw_piece(row, col, 1)
                    case -2:
                        self._draw_piece(row, col, 1, king=True)

        # Update turn coloring of labels
        if gamestate.turn == 0:
            self._player_1_label['fg'] = self._TURN_COL
            self._player_2_label['fg'] = 'black'
        else:
            self._player_1_label['fg'] = 'black'
            self._player_2_label['fg'] = self._TURN_COL


    def get_manual_input(
        self,
        moves: tuple[ppg.MoveType, ...]
    ) -> ppg.MoveType | None:
        """
        Return a user-selected move.

        Setting the `_manual` attribute to `True` prepares the `GUI` to
        receive user input. When the user inputs a move, it is saved
        into the `_manual_move` attribute, then returned next time this
        method is called.

        Parameters
        ----------
        moves : list of MoveType
            Valid `Move` instances the user can choose from.

        Returns
        -------
        MoveType, optional
        """

        if not self._manual:
            self._manual = True
            self._manual_move = None
            self._moves = moves
            self._set_valid()
        if self._manual_move is not None and self._manual:
            self._manual = False
            return self._manual_move
        return None

    def reset(self) -> None:
        """
        Reset persistent attributes to their initial values.
        """

        self._clear_valid()
        self._manual = False
        self._moves = ()
        self._manual_move = None
        if self._selected is not None:
            self._board_c.itemconfig(
                self._square_ref[self._selected],
                fill=self._DARK_COL
            )
            self._selected = None

        self._restart_game_button['relief'] = tk.RAISED
        self.restart_game_flag = False
        self._play_pause_button['relief'] = tk.RAISED
        self.pause_flag = False

    # Private methods

    def _draw_piece(
        self,
        row: int,
        col: int,
        team: int,
        king: bool = False
    ) -> None:
        """
        Draw the prescribed piece to the board.

        Parameters
        ----------
        row : int
            The row on the board to draw to.
        col : int
            The column on the board to draw to.
        team : {0, 1}
            The team of the piece; 0 is for black, 1 is for red.
        king : bool
            Whether or not the piece is a king; draws a golden inner
            circle to signify a king.

        Notes
        -----
        The id of the pieces on the `_board_c` Canvas object are saved
        to the `_piece_ref` attribute for reference to the corresponding
        rows and columns.
        """

        self._piece_ref[self._board_c.create_oval(
            col*self._SQUARE_PIX + self._PIECE_PAD,
            row*self._SQUARE_PIX + self._PIECE_PAD,
            (col+1)*self._SQUARE_PIX - self._PIECE_PAD,
            (row+1)*self._SQUARE_PIX - self._PIECE_PAD,
            fill='black' if team == 0 else 'red',
            tags='piece'
        )] = (row, col)
        if king:
            self._piece_ref[self._board_c.create_oval(
                col*self._SQUARE_PIX + self._KING_PAD,
                row*self._SQUARE_PIX + self._KING_PAD,
                (col+1)*self._SQUARE_PIX - self._KING_PAD,
                (row+1)*self._SQUARE_PIX - self._KING_PAD,
                fill='gold',
                tags='piece'
            )] = (row, col)

    def _clicked(self, event: tk.Event) -> None:
        """
        Click handler for manual move input.

        Only enabled when the `_manual` attribute is set to True.

        Parameters
        ----------
        event : Tk Event
        """

        if self._manual and not self.pause_flag:
            # Find row and column of click.
            widget_id = event.widget.find_withtag('current')[0]
            if widget_id in self._piece_ref:
                square = self._piece_ref[widget_id]
            else:
                square = self._board_ref[widget_id]
            self._set_highlights(square)

    def _restart_game(self) -> None:
        """
        Restart game button handler.

        Indicates to external runner that the game should be restarted.
        Part of this reset is calling the `reset` method or equivalent.
        """

        self.restart_game_flag = True

    def _play_pause(self) -> None:
        """
        Play pause button handler.

        Indicates to the external runner that the game loop should be
        paused until further notice.
        """

        if self.pause_flag:
            self._play_pause_button['relief'] = tk.RAISED
        else:
            self._play_pause_button['relief'] = tk.SUNKEN
        self.pause_flag = not self.pause_flag

    def _set_highlights(self, new_select: tuple[int, int]) -> None:
        """
        Square highlight handler.

        When the `GUI` instance is accepting manual input, valid squares
        and the currently selected square are highlighted.

        Parameters
        ----------
        new_select : tuple of int
            The (row, col) of the board selected by the user.
        """

        if new_select in self._valid and self._selected is not None:
            # Send selected move and reset.
            self._clear_valid()
            self._set_move(new_select)
            self._board_c.itemconfig(
                self._square_ref[self._selected],
                fill=self._DARK_COL
            )
            self._selected = None
        elif new_select in self._valid:
            # Start of move selected. Highlight squares to move to.
            self._clear_valid()
            self._set_valid(start=new_select)
            self._selected = new_select
            self._board_c.itemconfig(
                self._square_ref[self._selected],
                fill=self._SEL_COL
            )
        elif self._selected is not None and self._selected != new_select:
            # Deselect piece.
            self._board_c.itemconfig(
                self._square_ref[self._selected],
                fill=self._DARK_COL
            )
            self._selected = None
            self._clear_valid()
            self._set_valid()

    def _set_valid(self, start: tuple[int, int] | None = None) -> None:
        """
        Highlight squares that are valid to select.

        If there is no `start` argument, this highlights squares that
        contain pieces that can move. If there is a `start` argument,
        this highlights squares that the piece at `start` can jump to.

        Parameters
        ----------
        start : tuple of int, optional
        """

        for move in self._moves:
            assert isinstance(move, ppg.checkers.Move)
            if start is None:
                self._valid.append(move.start)
                self._board_c.itemconfig(
                    self._square_ref[move.start],
                    fill=self._VALID_COL
                )
            elif move.start == start:
                end_square = (
                    ppg.checkers.coord_sum(
                        ppg.checkers.coord_sum(move.start, move.d),
                        move.d
                    ) if move.capt else ppg.checkers.coord_sum(
                        move.start,
                        move.d
                    )
                )
                self._valid.append(end_square)
                self._board_c.itemconfig(
                    self._square_ref[end_square],
                    fill=self._VALID_COL
                )

    def _clear_valid(self):
        """
        Clear valid square highlighting.
        """

        for square in self._valid:
            self._board_c.itemconfig(
                self._square_ref[square],
                fill=self._DARK_COL
            )
        self._valid = []

    def _set_move(self, end: tuple[int, int]) -> None:
        """
        Convert user input into a checkers `Move` instance.

        Parameters
        ----------
        end : tuple of int
            The square of the end of the move.
        """

        for move in self._moves:
            assert isinstance(move, ppg.checkers.Move)
            square_1 = ppg.checkers.coord_sum(move.start, move.d)
            if move.start == self._selected and not move.capt:
                if end == square_1:
                    self._manual_move = move
                    break
            elif move.start == self._selected:
                square_2 = ppg.checkers.coord_sum(square_1, move.d)
                if end == square_2:
                    self._manual_move = move
                    break

    def _on_exit(self) -> None:
        """
        Tell client process that the `GUI` needs to be closed.

        Indirectly closing the `GUI` window allows for reliant processes
        to be terminated first.
        """

        self.terminated_flag = True
