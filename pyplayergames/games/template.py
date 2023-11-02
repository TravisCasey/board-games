"""
Protocols for games to interface with the package.

Each game defined should have a `Gamestate` class and a `Move` class
following these protocols. This ensures the games will integrate with
the agents, utilities, and each other in the `pyplayergames` package.
"""
# pylint: disable=C0116

from typing import Protocol, Self


class MoveType(Protocol):
    """
    Class structure for a move.
    """

    def __str__(self) -> str: ...
    # Represent `Move` object as a string.


class GamestateType(Protocol):
    """
    Class structure for a gamestate.

    Attributes
    ----------
    players : {2, 3, 4, ...}
        The number of players in the game.
    turn : {0, 1, 2, ..., `players`-1}
        The current player.
    valid_moves : list of MoveType instances
        Legal moves in the current state.
    score : tuple of floats
        Heuristic value of current state. Indexed by `turn` attribute.
        Higher scores are better.
    lower : float
        Lower bound on non-terminal `score` values.
    upper_sum : float
        Upper bound on the sum of non-terminal `score` values.
    reward : tuple of floats
        Value of terminal states. Indexed by `turn` attribute. Higher
        rewards are better.
    """

    players: int
    turn: int
    valid_moves: list[MoveType]
    score: tuple[float, ...]
    lower: float
    upper_sum: float
    reward: tuple[float, ...]

    def get_next(self, move: MoveType) -> Self: ...
    # Create new `Gamestate` according to the provided `move`.

    def is_game_over(self) -> bool: ...
    # Indicate if the game is over.

    def __hash__(self) -> int: ...
    # Define a hash function.
    #
    # Hashes are used for quick comparison of gamestates and for
    # transposition tables. Identical states must have the same hash.
    # Can be set to a uniform value to disable functionality.
