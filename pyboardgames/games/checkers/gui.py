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
    GOLD = (255, 205, 0)
    YELLOW = (255, 255, 0)
    GRAY = (127, 127, 127)
    SEL = (0, 255, 255, 100)
    VALID = (127, 255, 0, 127)
    SQ_PIX = 80
    WINDOW_SIZE = (8 * SQ_PIX, 9 * SQ_PIX)
    NEW_BUTTON = (int(5.5 * SQ_PIX),
                  int(8.25 * SQ_PIX),
                  2 * SQ_PIX,
                  SQ_PIX // 2)
    TEXT_SIZE = SQ_PIX // 3

    def __init__(self):
        """Initialize pygame, the window, widgets, and the game."""
        pygame.init()
        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('Checkers')
        self.clock = pygame.time.Clock()

        self.button_rect = pygame.Rect(self.NEW_BUTTON)
        self.button_text = pygame.font.Font(size=self.TEXT_SIZE)
        self.msg_text = pygame.font.Font(size=self.TEXT_SIZE)

        self.reset()
        self.draw_background()
        self.main_loop()

    def draw_background(self):
        """Draw the board on the background surface."""
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill(self.GRAY)
        for col in range(8):
            for row in range(8):
                color = self.LIGHT if col % 2 == row % 2 else self.DARK
                pygame.draw.rect(self.background, color,
                                 (col * self.SQ_PIX,
                                  row * self.SQ_PIX,
                                  self.SQ_PIX,
                                  self.SQ_PIX))

    def draw_pieces(self):
        """Draw the pieces according to the gamestate attribute."""
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

    def draw_menu(self):
        """Draw the new game button and text on the menu."""
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.window, self.YELLOW, self.NEW_BUTTON)
        else:
            pygame.draw.rect(self.window, self.GOLD, self.NEW_BUTTON)

        text_surf = self.button_text.render('New Game', True, self.BLACK)
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        self.window.blit(text_surf, text_rect)

        text_surf = self.button_text.render(self.msg, True, self.BLACK)
        text_rect = text_surf.get_rect(center=(int(1.5 * self.SQ_PIX), int(8.5*self.SQ_PIX)))
        self.window.blit(text_surf, text_rect)

    def reset(self):
        """Reset the game and window to the initial state."""
        self.move_tracker = []
        self.gamestate = CheckersGamestate()
        self.msg = "Red's move"

    def event_handler(self, event):
        """Handle user input and feed moves to gamestate.

        Args:
            event: A pygame event object to be handled by this method.
        """
        if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
            # User presses new game button.
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.reset()
            else:
                row = event.pos[1] // self.SQ_PIX
                col = event.pos[0] // self.SQ_PIX
                valid = False

                # Click on a valid square.
                for move in self.gamestate.valid_moves:
                    if (list(move[:len(self.move_tracker)+1])
                            == self.move_tracker + [(row, col)]):
                        if len(self.move_tracker) == len(move) - 1:
                            self.gamestate = self.gamestate.get_next(move)
                            self.move_tracker = []
                            if self.gamestate.is_game_over():
                                match self.gamestate.winner:
                                    case 1:
                                        self.msg = 'Red wins!'
                                    case 0:
                                        self.msg = 'Draw'
                                    case -1:
                                        self.msg = 'Black wins!'
                            else:
                                match self.gamestate.turn:
                                    case 1:
                                        self.msg = "Red's turn"
                                    case -1:
                                        self.msg = "Black's turn"
                        else:
                            if self.move_tracker:
                                self.msg = 'Jump again!'
                            self.move_tracker.append((row, col))
                        valid = True
                        break

                # Click off current move onto another valid square.
                if not valid:
                    for move in self.gamestate.valid_moves:
                        if move[0] == (row, col):
                            self.move_tracker = [(row, col)]
                            valid = True
                            break

                    # Click off current move onto an invalid square.
                    if not valid:
                        self.move_tracker = []

    def main_loop(self):
        """Run the graphical interface and detect user input."""
        run = True
        while run:
            self.clock.tick(60)
            self.window.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                else:
                    self.event_handler(event)

            self.draw_menu()
            self.draw_overlays()
            self.draw_pieces()

            pygame.display.flip()

        pygame.quit()

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
