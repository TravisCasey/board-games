"""Abstract classes used as templates for creating custom games.

At minimum, a new game must have the following classes, methods, and
attributes implemented for the provided agents to play the game. These
gamestates and moves should subclass these classes.
"""


from abc import ABC, abstractmethod


class GamestateTemplate(ABC):
    """Defines the class structure for a custom gamestate."""

    @property
    @abstractmethod
    def players(self):
        """Return the number of players in the game.

        Returns:
            A integer greater than or equal to two denoting the number
            of players playing the game.
        """

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

    @property
    @abstractmethod
    def valid_moves(self):
        """Return a collection of all legal moves.

        Returns:
            A list of instances of the proper subclass of the
            MoveTemplate abstract class defined for the game being
            played, that are legal moves for the current player to make.
        """
        pass

    @property
    @abstractmethod
    def turn(self):
        """Return an integer corresponding to the turn player.

        These integers should be indices of the score tuple. Thus the
        first player is 0, the second is 1, and so on.
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

    @property
    @abstractmethod
    def score(self):
        """Score the current position heuristically.

        Returns:
            A tuple indexed by the turn attribute. Entries are floats
            representing scores for the players at the current position.
            Greater scores indicate better positions.
        """
        pass

    @property
    @abstractmethod
    def upper(self):
        """The greatest obtainable non-terminal score.

        Used by the shallow pruning algorithm. Tighter bounds provide
        better pruning and thus better performance.

        Returns:
            A float that is greater than or equal to all possible scores
            returned by the score method on non-terminal positions.
        """
        pass

    @property
    @abstractmethod
    def lower(self):
        """The least obtainable non-terminal score.

        Used by the shallow pruning algorithm. Tighter bounds provide
        better pruning and thus better performance.

        Returns:
            A float that is less than or equal to all possible scores
            returned by the score method on non-terminal positions.
        """
        pass

    @property
    @abstractmethod
    def upper_sum(self):
        """An upper bound on the sum of scores of all players.

        Used by the pruning algorithms. Tighter bounds provide better
        pruning and thus better performance.

        Returns:
            A float that is greater than or equal to all possible sums
            of the scores of the players in all non-terminal positions.
        """
        pass


class MoveTemplate(ABC):
    """Defines the class structure for a custom move."""

    @abstractmethod
    def __str__(self):
        """Represent the move as a string.

        Used when expressed as part of a variation.

        Returns:
            A string representing the move when written out.
        """
        pass
