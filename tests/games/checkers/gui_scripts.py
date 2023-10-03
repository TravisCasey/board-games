"""Various scripts to run and test the checkers gui."""

from context import (gui,
                     RandomAgent,
                     IterativeDeepeningAgent,
                     ShallowPruningAgent,
                     IDDFSAgent,
                     MaxnAgent,
                     ParanoidAgent)
import sys

match sys.argv[1]:
    case '0': gui.CheckersGUI()
    case '1': gui.CheckersGUI(player1=RandomAgent())
    case '2': gui.CheckersGUI(player2=RandomAgent())
    case '3': gui.CheckersGUI(player1=RandomAgent(),
                              player2=RandomAgent())
    case '4': gui.CheckersGUI(player1=RandomAgent(),
                              a_time=0)
    case '11': gui.CheckersGUI(player1=IDDFSAgent(time=1.0),
                               player2=MaxnAgent(time=1.0))
    case '12': gui.CheckersGUI(player1=MaxnAgent(time=5.0, prune_enable=False),
                               player2=MaxnAgent(time=5.0))
    case '13': gui.CheckersGUI(player1=MaxnAgent(time=2.0, verbose=1),
                               player2=ParanoidAgent(time=2.0,
                                                     prune_enable=False,
                                                     verbose=1))
    case '14': gui.CheckersGUI(player1=ParanoidAgent(time=0.02,
                                                     verbose=1),
                               player2=ParanoidAgent(time=0.2, verbose=1))
