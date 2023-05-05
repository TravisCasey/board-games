from context import gui, RandomAgent
import sys

match sys.argv[1]:
    case '0': gui.CheckersGUI()
    case '1': gui.CheckersGUI(player1=RandomAgent())
    case '2': gui.CheckersGUI(player2=RandomAgent())
    case '3': gui.CheckersGUI(player1=RandomAgent(),
                              player2=RandomAgent())
