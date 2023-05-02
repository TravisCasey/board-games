"""Pygame graphical user interface for the checkers game.

Classes:
    CheckersGUI: An instance of the CheckersGUI class defines the
        the window, graphics, and runs the Checkers game. It has an
        associated CheckersGamestate object that handles the logic, and
        selects CheckersMove instances based on user input.
"""

import pygame
from pygame.locals import *
from pyboardgames.games.checkers.game import CheckersGamestate


class CheckersGUI():
    """The pygame graphical interface for the checkers game."""

    LIGHT = (255, 190, 125)
    DARK = (255, 127, 63)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GOLD = (255, 215, 0)
    SEL = (0, 255, 255, 100)
    VALID = (127, 255, 0, 127)
    SQ_PIX = 64
    BOARD_SIZE = (8 * SQ_PIX, 8 * SQ_PIX)

    def __init__(self):
        """Initialize pygame, the window, and the gamestate."""
        pygame.init()
        self.window = pygame.display.set_mode(self.BOARD_SIZE)
        pygame.display.set_caption('Checkers')
        self.clock = pygame.time.Clock()

        self.move_tracker = []
        self.gamestate = CheckersGamestate()
        self.result_display = False

        self.draw_background()
        self.event_loop()

    def draw_background(self):
        """Draws the board on the background surface."""
        self.background = pygame.Surface(self.window.get_size())
        for col in range(8):
            for row in range(8):
                color = self.LIGHT if col % 2 == row % 2 else self.DARK
                pygame.draw.rect(self.background, color,
                                 (row * self.SQ_PIX,
                                  col * self.SQ_PIX,
                                  (row + 1) * self.SQ_PIX,
                                  (col + 1) * self.SQ_PIX))

    def draw_pieces(self):
        """Draws the pieces according to the gamestate attribute."""
        for col in range(8):
            for row in range(8):
                center = (col * self.SQ_PIX + self.SQ_PIX // 2,
                          row * self.SQ_PIX + self.SQ_PIX // 2)
                match self.gamestate.board[row][col]:
                    case 1:
                        pygame.draw.circle(self.window,
                                           self.RED,
                                           center,
                                           self.SQ_PIX // 2)
                    case -1:
                        pygame.draw.circle(self.window,
                                           self.BLACK,
                                           center,
                                           self.SQ_PIX // 2)
                    case 2:
                        pygame.draw.circle(self.window,
                                           self.RED,
                                           center,
                                           self.SQ_PIX // 2)
                        pygame.draw.circle(self.window,
                                           self.GOLD,
                                           center,
                                           self.SQ_PIX // 4)
                    case -2:
                        pygame.draw.circle(self.window,
                                           self.BLACK,
                                           center,
                                           self.SQ_PIX // 2)
                        pygame.draw.circle(self.window,
                                           self.GOLD,
                                           center,
                                           self.SQ_PIX // 4)

    def event_loop(self):
        """Run the graphical interface and detect user input."""
        run = True
        while run:
            self.clock.tick(60)
            self.window.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                elif (event.type == MOUSEBUTTONDOWN
                      and event.button == BUTTON_LEFT):
                    if self.gamestate.is_game_over():
                        if self.result_display:
                            run = False
                        else:
                            self.result_display = True
                            match self.gamestate.winner:
                                case 1:
                                    pygame.display.set_caption('Team 1 wins')
                                case 0:
                                    pygame.display.set_caption('Draw')
                                case -1:
                                    pygame.display.set_caption('Team 2 wins')
                    else:
                        self.click_handler(event.pos[1] // self.SQ_PIX,
                                           event.pos[0] // self.SQ_PIX)

            self.draw_pieces()
            self.draw_overlays()
            pygame.display.flip()

        pygame.quit()

    def click_handler(self, row, col):
        """Determine meaning of left mouse button clicks.

        Args:
            row, col: which square the user clicked on.
        """
        valid = False
        for move in self.gamestate.valid_moves:
            if (list(move[:len(self.move_tracker)]) == self.move_tracker
                    and move[len(self.move_tracker)] == (row, col)):
                if len(self.move_tracker) == len(move) - 1:
                    self.gamestate = self.gamestate.get_next(move)
                    self.move_tracker = []
                else:
                    self.move_tracker.append((row, col))
                valid = True
                break
        if not valid:
            for move in self.gamestate.valid_moves:
                if move[0] == (row, col):
                    self.move_tracker = [(row, col)]
                    valid = True
                    break
        if not valid:
            self.move_tracker = []

    def highlight_square(self, row, col, color):
        """Overlay square with a semi-transparent color.

        Args:
            row, col: which square to highlight.
            color: 4 element tuple determing an RGB color and an alpha
                value for transparency.
        """
        surf = pygame.Surface((self.SQ_PIX, self.SQ_PIX), SRCALPHA)
        pygame.draw.rect(surf, color, surf.get_rect())
        self.window.blit(surf, (col * self.SQ_PIX,
                                row * self.SQ_PIX,
                                (col + 1) * self.SQ_PIX,
                                (row + 1) * self.SQ_PIX))

    def draw_overlays(self):
        """Determine which squares to highlight.

        Highlights both selected pieces and valid moves from selected
        piece.
        """
        if self.move_tracker:
            self.highlight_square(*self.move_tracker[-1], self.SEL)
            for move in self.gamestate.valid_moves:
                if list(move[:len(self.move_tracker)]) == self.move_tracker:
                    self.highlight_square(*move[len(self.move_tracker)],
                                          self.VALID)
