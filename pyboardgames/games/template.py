"""Abstract classes used as templates for creating custom games.

At minimum, a new game must have the following classes and methods
implemented for the provided agents to play the game. These gamestates
and moves should subclass these classes.
"""


from abc import ABC, abstractmethod


class GamestateTemplate(ABC):
    """Defines the class structure for a custom gamestate."""

    @abstractmethod
    def get_next(self, move):
        """Create a new gamestate according to the provided move.

        Args:
            move: An instance of a subclass of the MoveTemplate abstract
                class created for the game being played.

        Returns:
            A new instance of a subclass of the GamestateTemplate
            abstract class created for the game being played. This
            reflects the changes made by the provided move.
        """
        pass

    @abstractmethod
    def valid_moves(self):
        """Return a collection of all legal moves.

        Should be implemented with the property decorator.

        Returns:
            A list of instances of the proper subclass of the
            MoveTemplate abstract class defined for the game being
            played, that are legal moves for the current player to make.
        """
        pass

    @abstractmethod
    def winner(self):
        """Determine which player won the game, if any.

        Should be implemented with the property decorator.

        Returns:
            which player won.
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """Indicate if the game is over.

        Returns:
        True: game has ended.
        False: game has not ended.
        """
        pass


class MoveTemplate(ABC):
    """Defines the class structure for a custom move."""

    pass
