import time
from collections import deque
from pyboardgames.agents.template import AgentTemplate


class Node():

    def __init__(self, gamestate, parent=None):
        self.parent = parent
        self.gamestate = gamestate
        self.score = 0


class IterativeDeepeningAgent(AgentTemplate):
    """A DFS minimax agent that uses iterative deepening."""

    def __init__(self, name, time=0.0):
        self.name = name
        self.time = time
        self.queue = deque()

    def get_move(self, gamestate):


    def depth_limited_search(self, gamestate, depth):
        if depth == 0:
            return gamestate.score

        
