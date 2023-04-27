"""Abstract classes used as templates for creating custom games.

Classes:
    GamestateTemplate: Defines the class structure that must be
        implemented for custom gamestates in order for the agents to
        play the game.
    MoveTemplate: Defines the class structure for moves of a certain
        game.
"""

from abc import ABC, abstractmethod


class GamestateTemplate(ABC):

    @abstractmethod
    def update(self, move):
        """Updates the gamestate according to the provided move.

        Args:
            move: An instance of a subclass of the MoveTemplate abstract
                class created for the game being played.
        """
        pass

    @abstractmethod
    def valid_moves(self):
        """This property is a collection of all legal moves.

        Should be implemented with the property decorator.

        Returns:
            A list of instances of the proper subclass of the
            Template abstract class defined for the game being played,
            that are legal moves for the current player to make.
        """
        pass

    @abstractmethod
    def winner(self):
        """Determines which player won the game, if any.

        Should be implemented with the property decorator.

        Returns:
        1: Team 1 won.
        -1: Team 2 won.
        0: Draw
        None: The game has not ended.
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """Indicates if the game is over.

        Returns:
        True: game has ended.
        False: game has not ended.
        """
        pass

    @abstractmethod
    def copy(self):
        """Returns a deep copy of the currnet state.

        Returns:
            An identical but distinct object as the instance with this
            method.
        """
        pass


class MoveTemplate(ABC):
    pass
