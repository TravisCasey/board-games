import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..\\..\\..')))
print(sys.path)

from pyboardgames.games.checkers import game