# N-player games with deep reinforcement learning
This repo is a collection of playable games along with agents designed to play the board games. Custom games can be defined using the provided template that has the minimum attributes and functions required for the agents to play the game. Currently, checkers and an abstract 'game' defined directly using a tree are implemented; the latter is used for testing purposes. There are a variety of agents deisgned to play the games, including DFS algorithms, Monte Carlo tree search, and deep Q-learning. A proof of concept build concerned with only checkers can be found in my [checkers ai repo](https://github.com/TravisCasey/checkers-ai).

The goal of this endeavour is an exploration into the strengths and weaknesses of various decision tree agents, and how this may vary from type of game, number of players, time constraints, etc. It is also a useful abstraction of what defines an agent and a game in a general enough context that most games can be successfully implemented, but regular enough that all the agents can play the games without modification. 

A work in progress.
