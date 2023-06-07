"""Agent classes employing forms of the minimax algorithm."""

import time
import random
from pyboardgames.agents.template import AgentTemplate


class IterativeDeepeningAgent(AgentTemplate):
    """A DFS minimax agent that uses iterative deepening.

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

        self.player = None
        self.time_start = None
        self.complete = True

    def get_move(self, gamestate):
        """Find the next best move by employing max^n.

        Depth searched starts at 1, and increments as far as possible
        based on allotted time.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
        """
        if len(gamestate.valid_moves) == 1:
            # No need to search if there is only one move.
            return gamestate.valid_moves[0]

        # Set instance variables
        self.time_start = time.time()
        self.player = gamestate.turn

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
                        and score[self.player] < max_score[self.player]):
                    max_score = score

        return max_score
