"""
Abstract
========

This module contains the logic and implementation for an abstracted
tree-based game, intended for testing purposes.

"""

from __future__ import annotations
from typing import Any
import pyplayergames as ppg


class Edge(ppg.MoveType):
    """
    Abstract move class.

    Effectively a wrapper for an integer; the integer is an index
    to move from one vertex to one of the next vertices in the tree.

    Parameters
    ----------
    index : {0, 1, 2, ...}
        The index of the next vertex to move to.

    Raises
    ------
    TypeError
        If `index` is not an integer.
    ValueError
        If `index` is a negative integer.

    """

    def __init__(self, index: int) -> None:

        if not isinstance(index, int):
            raise TypeError('Expected index input as an integer.')
        if index < 0:
            raise ValueError('index should be nonnegative.')

        self._index: int = index

    def __str__(self) -> str:
        """
        Return the index as a string.
        """

        return str(self._index)

    def __int__(self) -> int:
        """
        Return the index.
        """

        return self._index


class Node(ppg.GamestateType):
    """
    Abstract gamestate class.

    Defines a custom abstract game tree for one or more players. A
    `Node` object encodes the gamestate attributes as well as references
    to the next possible gamestates.

    Parameters
    ----------
    children : tuple of `Node`
        The children `Node` instances of the current instance.
    players : {1, 2, 3, ...}
        The number of players in the game. Should be constant throughout
        the game.
    turn : {0, 1, 2, ..., `players`-1}
        The turn at the current node. Indexes the score tuple and the
        reward tuple.
    score : tuple of float
        The assigned score at the current node. Indexed by the `turn`
        attrbiute.
    lower : float
        The lowest attainable non-terminal score. Should be constant
        throughout the game.
    upper_sum : float
        The greatest attainable non-terminal sum of scores. Should be
        constant throughout the game.

    """

    def __init__(
        self,
        children: tuple[Node, ...],
        players: int,
        turn: int,
        score: tuple[float, ...],
        lower: float,
        upper_sum: float
    ) -> None:

        self._children: tuple[Node, ...] = children
        self.players: int = players
        self._turn: int = turn
        self._score: tuple[float, ...] = score
        self.lower: float = lower
        self.upper_sum: float = upper_sum

    @classmethod
    def build_tree(
        cls,
        players: int,
        lower: float,
        upper_sum: float,
        turn: int,
        score: tuple[float, ...],
        *subtrees: list[Any]
        ) -> Node:
        """
        Constructor method for building tree from list representation.

        List representation of a tree is recursive; the first elements
        of the list are the turn and score values, respectively. The
        remaining elements are lists encoding the subtrees; these follow
        the same representation as above. Terminal nodes have no
        subtrees.

        Parameters
        ----------
        players : int
        lower : float
        upper_sum : float
        turn : {0, 1, 2, ..., players-1}
        score : tuple of float
        *subtrees : list of turn, score, and subtrees

        Examples
        --------
        >>> tree_list = [0, (2.0, 0.0, 1.0),
        ...              [1, (0.0, 0.0, 10.0),
        ...               [2, (1.0, 1.0, 4.0)],
        ...               [2, (0.0, 0.0, 10.0)]],
        ...              [1, (2.0, 2.0, 1.0)],
        ...              [1, (3.0, 0.0, 0.0)]]
        >>> ppg.abstract.Node.build_tree(
        ...     3,
        ...     0.0,
        ...     10.0,
        ...     *tree_list
        ... )

        """
        return Node(
            tuple(cls.build_tree(players, lower, upper_sum, *subtree)
                  for subtree in subtrees),
            players,
            turn,
            score,
            lower,
            upper_sum
        )

    # Interface

    @property
    def turn(self) -> int:
        """
        Return the index of the current turn player.
        """

        return self._turn

    def get_moves(self) -> tuple[ppg.MoveType, ...]:
        """
        Return a list of all valid `Edge` instances from the node.
        """

        return tuple(Edge(i) for i in range(len(self._children)))


    def get_next(self, move: ppg.MoveType) -> Node:
        """
        Return the next `Node` instance corresponding to the move input.

        As this is primarily used for testing, this does not check for
        validity of the move. Errors or unexpected behavior may occur.

        Parameters
        ----------
        move : Edge

        Returns
        --------
        Node
        """

        assert isinstance(move, Edge)
        return self._children[int(move)]

    def is_game_over(self) -> bool:
        """
        Return True if the game is over and False otherwise.

        Game is defined to be over when the current `Node` instance has
        no children.
        """

        return not self._children

    def get_score(self) -> tuple[float, ...]:
        """
        Return assigned value of current node.
        """
        return self._score

    def get_reward(self) -> tuple[float, ...]:
        """
        Return value of terminal states.

        Reward values are calculated by designating the player with the
        highest score at a terminal position as the winner; the winner
        takes all. Ties split the reward.
        """

        if not self.is_game_over():
            raise AttributeError(
                'Reward attribute referenced before game is over.'
            )

        max_score = max(self._score)
        ties = self._score.count(max_score)
        value = 1.0 / ties
        reward = []
        for score in self._score:
            if score == max_score:
                reward.append(value)
            else:
                reward.append(0.0)
        return tuple(reward)

    def __hash__(self) -> int:
        """
        Hashing disabled for abstract game.
        """

        return 0
