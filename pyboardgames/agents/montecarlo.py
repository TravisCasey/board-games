"""Monte Carlo tree search agent and supporting classes/functions."""

import time
import random
import math
from pyboardgames.agents.template import AgentTemplate


class Node():
    """Gamestate wrapper for game tree organization."""

    def __init__(self, gamestate, move):
        """Define the node and its attributes at the given gamestate.

        Args:
            gamestate: An instance of the gamestate class being played.
            move: The instance of the associated move class used to
                reach the gamestate.
        """
        self.gamestate = gamestate
        self.move = move

        # Traversal attributes
        self.terminal = self.gamestate.is_game_over()
        self._children = []

        # Monte Carlo attributes
        self.visits = 0
        self.rewards = 0

    @property
    def children(self):
        """Calculate and instantiate children nodes."""
        if not self._children and not self.terminal:
            self._children = [Node(self.gamestate.get_next(move), move)
                              for move in self.gamestate.valid_moves]
        return self._children

    def is_leaf(self):
        """Determine if the Node has unexplored children.

        Returns:
            True if there exists a child Node that has 0 visits and
            false otherwise.
        """
        for child in self.children:
            if child.visits == 0:
                return True
        return False


class MCTSAgent(AgentTemplate):
    """An agent employing Monte Carlo tree search (MCTS)."""

    def __init__(self,
                 name='MCTS Agent',
                 time=30.0,
                 ucb_param=math.sqrt(2.0),
                 verbose=0):
        """Create instance of the agent and set initial attributes.

        Args:
            name: A string keyword argument that sets a display name for
                the agent.
            time: A float keyword argument for the time in seconds for
                the agent to pick a move.
            ucb_param: A float keyword argument used in the UCT
                calculation.
            verbose: An integer keyword argument that sets the verbosity
                of the agent. The values indicate:
                - 0: No console output.
                - 1: Prints the best move, and number of simulations run
                    when returning the best move found.
                - 2: As in 1 but includes timing information.
        """
        self.name = name
        self.time = time
        self._ucb_param = ucb_param
        self._verbose = verbose

        self.reset()

    def reset(self):
        """Return agent to initial state."""
        self._time_ini = None

    def get_move(self, gamestate):
        """Select the best move through sampling the game tree.

        Args:
            gamestate: An instance of the gamestate class being played
                from which to search.

        Returns:
            An instance of the move class corresponding to the best
            move found by the agent.
        """
        self._time_ini = time.time()
        self._turn = gamestate.turn
        root = Node(gamestate, None)
        while (time.time() - self._time_ini) < self.time:
            self.traverse(root)
        best_child = None
        most_visits = 0
        for child in root.children:
            if child.visits > most_visits:
                best_child = child
                most_visits = child.visits
        self.console_output(best_child.move, root.visits, root.rewards)
        return best_child.move

    def traverse(self, node):
        """Recursively traverse the game tree to select rollout node.

        Args:
            node: The node to start selecting from, and to update
                the attributes of after rollout.

        Return:
            A float indicating the reward found for the agent at the end
            of the rollout.
        """
        # Unexplored children
        if node.is_leaf():
            rollout_root = random.choice([child for child in node.children
                                          if child.visits == 0])
            sim_reward = self.simulate(rollout_root)
            rollout_root.visits += 1
            rollout_root.rewards += sim_reward

        # Selection finds terminal node.
        elif node.terminal:
            sim_reward = node.gamestate.reward[self._turn]

        # Select next node according to ucb value and backpropagate the
        # reward found.
        else:
            sim_reward = self.traverse(self.ucb_choice(node))

        # Update node attributes with reward.
        node.visits += 1
        node.rewards += sim_reward

        # Backpropagate
        return sim_reward

    def ucb_choice(self, node):
        """Chooses child based on Upper Confidence Bound (UCB) score.

        Do not call on a leaf node or terminal node.

        Args:
            node: An instance of the Node class that is not a leaf or
                terminal node. Chooses from among its children.

        Returns:
            A Node instance corresponding to the child of the node arg
            with the greatest UCB score.
        """
        best_ucb = float('-inf')
        for child in node.children:
            exploit = child.rewards / child.visits
            explore = math.sqrt(math.log(node.visits) / child.visits)
            ucb = exploit + self._ucb_param * explore
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child
        return best_child

    def simulate(self, node):
        """Simulate game from given node using random moves.

        Args:
            node: An instance of the node class wrapping the gamestate
                to simulate from.

        Returns:
            Float indicating the reward for the agent from this
            simulation.
        """
        sim_state = node.gamestate
        while not sim_state.is_game_over():
            sim_move = random.choice(sim_state.valid_moves)
            sim_state = sim_state.get_next(sim_move)
        return sim_state.reward[self._turn]

    def console_output(self, move, visits, reward):
        """Output data to console for debugging and logging."""
        if self._verbose > 0:
            print('----------------------')
            print(self.name)
            print('----------------------')
            print('Best move: {}'.format(move))
            print('Simulations: {}'.format(visits))
            print('Average reward: {:.3f}'.format(reward / visits))
        if self._verbose > 1:
            time_diff = time.time() - self._time_ini
            print('Time elapsed: {:.3f}'.format(time_diff))
            print('Average simulation time: {:.4f}'.format(time_diff / visits))
        if self._verbose > 0:
            print('----------------------\n')
