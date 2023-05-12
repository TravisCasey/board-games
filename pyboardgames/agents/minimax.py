"""Agent classes employing forms of the minimax algorithm."""

import time
import random
from pyboardgames.agents.template import AgentTemplate


class IterativeDeepeningAgent(AgentTemplate):
    """A DFS minimax agent that uses iterative deepening."""

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

    def get_move(self, gamestate):
        """Find the next best move.

        Current operating at a fixed depth; in the future, this will be
        iterative and based off time.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
        """
        self.start_time = time.time()
        self.time_up = False

        depth = 1
        saved_move = gamestate.valid_moves[0]
        if len(gamestate.valid_moves) == 1:
            return saved_move
        while True:
            best_score = float('-inf')
            best_moves = []
            for move in gamestate.valid_moves:
                score_tup = self.depth_search(gamestate.get_next(move),
                                              depth-1)
                if self.time_up:
                    break
                else:
                    score = score_tup[gamestate.turn]
                    if score > best_score:
                        best_score = score
                        best_moves = [move]
                    elif score == best_score:
                        best_moves.append(move)
            if self.time_up:
                break
            else:
                saved_move = random.choice(best_moves)
                if best_score == float('inf') or best_score == float('-inf'):
                    break
            depth += 1
        return saved_move

    def depth_search(self, gamestate, depth):
        """Search the tree for the next best move to a given depth.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the tree starting from this gamestate.
            depth: The number of plies to search forward.
        """
        if time.time() - self.start_time > self.time:
            self.time_up = True
        if self.time_up:
            return
        if depth == 0 or gamestate.is_game_over():
            return gamestate.score
        else:
            move = gamestate.valid_moves[0]
            max_score = self.depth_search(gamestate.get_next(move), depth-1)
            if self.time_up:
                return
            max_value = max_score[gamestate.turn]
            for move in gamestate.valid_moves[1:]:
                score = self.depth_search(gamestate.get_next(move), depth-1)
                if self.time_up:
                    return

                if score[gamestate.turn] > max_value:
                    max_value = score[gamestate.turn]
                    max_score = score
                elif score[gamestate.turn] == max_score:
                    # Find worst-case scenario
                    for turn in range(1, len(score) - 1):
                        if score[turn] < max_score[turn]:
                            max_score = score
                            break
                        elif score[turn] < max_score[turn]:
                            break
            return max_score
