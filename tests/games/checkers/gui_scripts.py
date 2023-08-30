"""Various scripts to run and test the checkers gui."""

from context import (gui,
                     RandomAgent,
                     IterativeDeepeningAgent,
                     ShallowPruningAgent)
import sys

match sys.argv[1]:
    case '0': gui.CheckersGUI()
    case '1': gui.CheckersGUI(player1=RandomAgent())
    case '2': gui.CheckersGUI(player2=RandomAgent())
    case '3': gui.CheckersGUI(player1=RandomAgent(),
                              player2=RandomAgent())
    case '4': gui.CheckersGUI(player1=RandomAgent(),
                              a_time=0)
    case '5': gui.CheckersGUI(player2=IterativeDeepeningAgent(time=10))
    case '6': gui.CheckersGUI(player1=RandomAgent(),
                              player2=IterativeDeepeningAgent())
    case '7': gui.CheckersGUI(player1=IterativeDeepeningAgent(time=3.0),
                              player2=RandomAgent())
    case '8': gui.CheckersGUI(player1=IterativeDeepeningAgent(time=3.0),
                              player2=IterativeDeepeningAgent(time=1.0))
    case '9': gui.CheckersGUI(player1=ShallowPruningAgent(time=3.0),
                              player2=RandomAgent())
    case '10': gui.CheckersGUI(player1=ShallowPruningAgent(time=10),
                               player2=IterativeDeepeningAgent(time=10))
