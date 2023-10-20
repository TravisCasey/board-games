"""Gamestate and move class for and abstract game tree.

Defines a custom game tree for testing purposes.
"""

from pyboardgames.games.template import GamestateTemplate, MoveTemplate


class Edge(MoveTemplate):
    """An edge in the abstract game tree.

    Effectively a wrapper for an integer; the integer is an index
    to move from one vertex to one of the next vertices.
    """

    def __init__(self, index):
        """Initialize edge.

        Args:
            index: A positive integer corresponding to the index
                of the vertex to move to.

        Raises:
            TypeError: If index is not an integer.
            ValueError: If index is nonpositive.
        """
        if type(index) is not int:
            raise TypeError('Expected index input as an integer.')
        if index <= 0:
            raise ValueError('index should be positive.')

        self._index = index

    def __str__(self):
        """Return the index as a string."""
        return str(self._index)

    def __int__(self):
        """Return the index."""
        return self._index


class Tree(GamestateTemplate):
    """Defines a custom abstract game tree for two or more players.

    Assumes turns alternate between the players in order. Tree is
    endcoded as a list of lists with a tuple of values at each node,
    representing the heuristic score at that node.

    Example: Consider the following tree for 3 players, with vertex
    values and edges labeled:

                                (1, 1, 1)
                                /       |
                             1 /        | 2
                              /         |
                        (1, 4, 4)       (0, 1, 2)
                        /     |            /    |
                     1 /      | 2       1 /     | 2
                      /       |          /      |
             (2, 3, 0)  (1, 1, 0)  (4, 0, 4)  (1, 1, 1)

    It has the following list representation:
    [(1.0, 1.0, 1.0),
        [(1.0, 4.0, 4.0),
         [(2.0, 3.0, 0.0)],
         [(1.0, 1.0, 0.0)]],
        [(0.0, 1.0, 2.0),
         [(4.0, 0.0, 4.0)],
         [(1.0, 1.0, 1.0)]]]
    """

    def __init__(self, tree, players, upper, lower, upper_sum, turn=0):
        """Initialize the game tree.

        Args:
            tree: A list of lists representing a game tree as in the
                class docstring.
            players: An integer number of players.
            upper: A float that is the maximum score at the non-terminal
                vertices.
            lower: A float that is the minimum score at the non-terminal
                vertices.
            upper_sum: A float that is the maximum sum of all players
                scores at non-terminal vertices.
            turn: An integer index corresponding to the current turn.
                First player is 0, second is 1, and so on.
        """
        self.tree = tree
        self._players = players
        self._upper = upper
        self._lower = lower
        self._upper_sum = upper_sum
        self._turn = turn
        self._reward = None

    @property
    def players(self):
        """Return the number of players."""
        return self._players

    @property
    def upper(self):
        """Return the highest obtainable non-terminal score."""
        return self._upper

    @property
    def lower(self):
        """Return the least obtainable non-terminal score."""
        return self._lower

    @property
    def upper_sum(self):
        """Return the highest obtainable sum of all scores."""
        return self._upper_sum

    @property
    def turn(self):
        """Return the index of the current turn player."""
        return self._turn

    def get_next(self, move):
        """Create a subtree object corresponding to the move input.

        As this is primarily used for testing, this does not check for
        validity of the move. Errors or unexpected behavior may occur.

        Args:
            move: An instance of the Edge class determining which
                subtree to move to.

        Returns:
            A new instance of the Tree class corresponding to the
                subtree moved to by the provided move.
        """
        next_turn = self.turn + 1
        if next_turn == self.players:
            next_turn = 0

        return Tree(self.tree[int(move)],
                    self.players,
                    self.upper,
                    self.lower,
                    self.upper_sum,
                    next_turn)

    @property
    def valid_moves(self):
        """Return a list of all legal moves.

        Returns:
            A list of Edge instances that lead to other vertices in
            the tree from the current vertex.
        """
        return [Edge(i) for i in range(1, len(self.tree))]

    def is_game_over(self):
        """Return True if the game is over and False otherwise."""
        return (len(self.tree) == 1)

    @property
    def reward(self):
        """Reward players based on score in the terminal node.

        Winner takes all method or 1.0 reward is evenly split among
        those tying for first.
        """
        if self._reward is not None:
            return self._reward

        reward_tup = (0,) * self.players
        best_score = float('-inf')
        best_players = []
        for player in range(self.players):
            if self.tree[0][player] > best_score:
                best_score = self.tree[0][player]
                best_players = [player]
            elif self.tree[0][player] == best_score:
                best_players.append(player)

        split_reward = 1.0 / len(best_players)
        for player in best_players:
            reward_tup[player] = split_reward
        return reward_tup

    @property
    def score(self):
        """Return the value of the current vertex of the tree."""
        return self.tree[0]
