"""Abstract classes used as templates for creating custom agents.

At minimum, a new agent must sublcass the following class and have the
methods below implemented for the to play the games.
"""

from abc import ABC, abstractmethod


class AgentTemplate(ABC):
    """Defines the class structure for a custom gamestate."""

    @abstractmethod
    def __init__(self, time=0.0):
        """Initialize the agent.

        Args:
            time: Agents should handle the keyword argument for time.
                This is a float representing the time in seconds the
                agent has to work before it must pick a move. The
                default value is 0.0, which should indicate the agent
                has no time limit.
        """
        pass

    @abstractmethod
    def get_move(self, gamestate):
        """Choose the next move.

        Args:
            gamestate: An object representing the gamestate from which
                the agent should determine the next move.

        Returns:
            An object representing the chosen move.
        """
        pass
