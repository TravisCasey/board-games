"""
Protocols for interfacing with the `pyplayergames` package.
"""
# pylint: disable=C0116

from __future__ import annotations
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
    players : {1, 2, 3, 4, ...}
        The number of players in the game.
    lower : float
        Lower bound on non-terminal `score` values.
    upper_sum : float
        Upper bound on the sum of non-terminal `score` values.
    """

    players: int
    lower: float
    upper_sum: float

    @property
    def turn(self) -> int: ...
    # The current player. Value indexes the score and reward attributes.

    def get_moves(self) -> tuple[MoveType, ...]: ...
    # Return a list of all legal moves from the current `Gamestate`.

    def get_next(self, move: MoveType) -> Self: ...
    # Create new `Gamestate` according to the provided `move`.

    def is_game_over(self) -> bool: ...
    # Indicate if the game is over.

    def get_score(self) -> tuple[float, ...]: ...
    # Heuristic value of the current state, indexed by `get_turn`.
    # Need only consider non-terminal states.
    # Higher values are better.

    def get_reward(self) -> tuple[float, ...]: ...
    # Value of terminal states, indexed by `get_turn`.
    # Higher values are better.

    def __hash__(self) -> int: ...
    # Define a hash function.
    #
    # Hashes are used for quick comparison of gamestates and for
    # transposition tables. Identical states must have the same hash.
    # Can be set to a uniform value to disable functionality.


class MatchType(Protocol):
    """
    Class structure for a match.
    """

    result: tuple[float, ...]

    def __init__(self,
                 agents: tuple[AgentType | None, ...],
                 **kwargs
                 ) -> None: ...

    def run(self) -> None: ...

class AgentType(Protocol):
    """
    Class structure for an agent.
    """

    name: str

    def __init__(self, **kwargs) -> None: ...

    def get_move(self, gamestate: GamestateType) -> MoveType: ...
    # Choose the next move.

    def reset(self) -> None: ...
    # Reset agent to its original state.
