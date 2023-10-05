"""Abstract classes used as templates for creating custom agents.

At minimum, a new agent must sublcass the following class and have the
methods below implemented to play the games.
"""

from abc import ABC, abstractmethod


class AgentTemplate(ABC):
    """Defines the class structure for a custom gamestate."""

    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the agent.

        Args:
            name: A descriptive name for the agent to be displayed on
                the gui.
            time: Agents should handle the keyword argument for time.
                This is a float representing the time in seconds the
                agent has to work before it must pick a move. Time 0.0,
                indicates the agent has no time limit.
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

    @abstractmethod
    def reset(self):
        """Reset the agent to its initial state for a new game."""
        pass
