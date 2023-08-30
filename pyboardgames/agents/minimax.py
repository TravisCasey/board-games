"""Agent classes employing forms of the minimax algorithm."""

import time
import random
from pyboardgames.agents.template import AgentTemplate


class IterativeDeepeningAgent(AgentTemplate):
    """A DFS agent using iterative deepening.

    Implements the max^n algorithm with no pruning for n players, which
    reduces to minimax in the case n=2. See details at:
    https://cdn.aaai.org/AAAI/1986/AAAI86-025.pdf.
    """

    def __init__(self, **kwargs):
        """Initialize the agent.

        Args:
            name: A keyword argument that sets a name for the agent.
            time: A keyword argument representing the time in seconds
        """
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'IDS Player'
        if 'time' in kwargs:
            self.time = kwargs['time']
        else:
            self.time = 30.0

        self.root_turn = None
        self.time_start = None
        self.complete = True

    def get_move(self, gamestate):
        """Find the best move using iterative deepening max^n.

        Depth searched starts at 1, and increments as far as possible
        based on allotted time.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
        """
        # No need to search if there is only one move.
        if len(gamestate.valid_moves) == 1:
            return gamestate.valid_moves[0]

        # Set instance variables
        self.time_start = time.time()
        self.root_turn = gamestate.turn

        # Default move is random; search should improve on this.
        saved_move = random.choice(gamestate.valid_moves)

        depth = 1
        while True:
            self.complete = True  # Tree complete until shown otherwise.
            max_score = float('-inf')
            best_moves = []

            for move in gamestate.valid_moves:
                # Score each child of the parent gamestate.
                score = self.depth_score(gamestate.get_next(move), depth-1)

                # None score indicates out of time; return the most
                # recently selected move.
                if score is None:
                    return saved_move

                # Collect moves that gaurentee the best score.
                if score[gamestate.turn] > max_score:
                    max_score = score[gamestate.turn]
                    best_moves = [move]
                elif score[gamestate.turn] == max_score:
                    best_moves.append(move)

            # Break ties randomly.
            saved_move = random.choice(best_moves)

            # If the game tree has been fully explored, no more search
            # is required.
            if self.complete:
                return saved_move

            # Iterate depth value.
            depth += 1

    def depth_score(self, gamestate, depth):
        """Score the gamestate by analyzing the tree to a set depth.

        Uses max^n algorithm with ties broken first by assuming that
        opponents will seek to also minimize the score of the player
        represented by the object. See
        https://webdocs.cs.ualberta.ca/~nathanst/papers/comparison_algorithms.pdf.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
            depth: The number of plies to search forward.
        """
        if time.time() - self.time_start >= self.time:
            # Out of time.
            return None
        elif gamestate.is_game_over():
            # Terminal node; use scoring heuristic.
            return gamestate.score
        elif depth == 0:
            # Use scoring heuristic and note tree as incomplete
            self.complete = False
            return gamestate.score
        else:
            # Initialize score trackers
            move = gamestate.valid_moves[0]
            max_score = self.depth_score(gamestate.get_next(move), depth-1)

            # Out of time.
            if max_score is None:
                return None

            # Score the next depth, updating score trackers as needed.
            for move in gamestate.valid_moves[1:]:
                score = self.depth_score(gamestate.get_next(move), depth-1)
                # Out of time.
                if score is None:
                    return None
                if score[gamestate.turn] > max_score[gamestate.turn]:
                    max_score = score
                elif (score[gamestate.turn] == max_score[gamestate.turn]
                        and score[self.root_turn] < max_score[self.root_turn]):
                    max_score = score

        return max_score


class ShallowPruningAgent(AgentTemplate):
    """A DFS agent using iterative deepening and shallow pruning.

    Implements the max^n algorithm with shallow pruning. This is optimal
    pruning for the max^n algorithm with more than 2 players; see
    https://faculty.cc.gatech.edu/~thad/6601-gradAI-fall2015/Korf_Multi-player-Alpha-beta-Pruning.pdf
    for details.
    """

    def __init__(self, **kwargs):
        """Initialize the agent.

        Args:
            name: A keyword argument that sets a name for the agent.
            time: A keyword argument representing the time in seconds
        """
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'Shallow Pruning Player'
        if 'time' in kwargs:
            self.time = kwargs['time']
        else:
            self.time = 30.0

        self.root_turn = None
        self.time_start = None
        self.complete = True

    def get_move(self, gamestate):
        """Find the best move using iterative deepening max^n.

        Depth searched starts at 1, and increments as far as possible
        based on allotted time.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
        """
        # No need to search if there is only one move.
        if len(gamestate.valid_moves) == 1:
            return gamestate.valid_moves[0]

        # Set instance variables
        self.time_start = time.time()
        self.root_turn = gamestate.turn

        # Default move is random; search should improve on this.
        saved_move = random.choice(gamestate.valid_moves)

        depth = 1
        while True:
            self.complete = True  # Tree complete until shown otherwise.
            best_moves = [gamestate.valid_moves[0]]
            max_score = self.shallow_score(gamestate.get_next(best_moves[0]),
                                           depth-1,
                                           gamestate.upper)
            if max_score is None:
                return saved_move

            for move in gamestate.valid_moves[1:]:
                # Score each child of the parent gamestate.
                next_bound = gamestate.upper - max_score[gamestate.turn]
                score = self.shallow_score(gamestate.get_next(move),
                                           depth-1,
                                           next_bound)

                # None score indicates out of time; return the most
                # recently selected move.
                if score is None:
                    return saved_move

                # Collect moves that gaurentee the best score.
                if score[gamestate.turn] > max_score[gamestate.turn]:
                    max_score = score
                    best_moves = [move]
                elif score[gamestate.turn] == max_score[gamestate.turn]:
                    best_moves.append(move)

            # Break ties randomly.
            saved_move = random.choice(best_moves)

            # If the game tree has been fully explored, no more search
            # is required.
            if self.complete:
                return saved_move

            # Iterate depth value.
            depth += 1

    def shallow_score(self, gamestate, depth, bound):
        """Score the gamestate by analyzing the tree to a set depth.

        Uses max^n algorithm with shallow pruning. Ties are broken first
        by assuming that opponents will seek to also minimize the score
        of the player represented by the object. See
        https://webdocs.cs.ualberta.ca/~nathanst/papers/comparison_algorithms.pdf.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
            depth: The number of plies to search forward.
            bound: The upper bound on scores; higher scores are pruned.
        """
        if time.time() - self.time_start >= self.time:
            # Out of time.
            return None
        elif gamestate.is_game_over():
            # Terminal node; use scoring heuristic.
            return gamestate.score
        elif depth == 0:
            # Use scoring heuristic and note tree as incomplete
            self.complete = False
            return gamestate.score
        else:
            # Initialize score trackers
            move = gamestate.valid_moves[0]
            max_score = self.shallow_score(gamestate.get_next(move),
                                           depth-1,
                                           gamestate.upper)

            # Out of time.
            if max_score is None:
                return None

            # Score the next depth, updating score trackers as needed.
            for move in gamestate.valid_moves[1:]:
                if max_score[gamestate.turn] >= bound:
                    return max_score

                next_bound = gamestate.upper - max_score[gamestate.turn]
                score = self.shallow_score(gamestate.get_next(move),
                                           depth-1,
                                           next_bound)
                # Out of time.
                if score is None:
                    return None
                if score[gamestate.turn] > max_score[gamestate.turn]:
                    max_score = score
                elif (score[gamestate.turn] == max_score[gamestate.turn]
                        and score[self.root_turn] < max_score[self.root_turn]):
                    max_score = score

        return max_score
