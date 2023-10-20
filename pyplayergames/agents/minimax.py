"""Agent classes employing forms of the minimax algorithm."""

import time
import random
from collections import OrderedDict
from pyplayergames.agents.template import AgentTemplate

# TODO: add reset for new game.


class IDDFSAgent(AgentTemplate):
    """A DFS agent that uses iterative deepening to find the best move.

    The agent iterates through the game tree in a DFS manner to a set
    depth. After exploring the tree to this depth, the agent chooses the
    best move based upon some scoring algorithm. It then increments the
    depth and searches again. If the agent runs out of time, it returns
    the most recently chosen move.

    This class is a base class for the other DFS agents in this module.
    """

    def __init__(self,
                 name='DFS Agent',
                 time=30.0,
                 prune_enable=True,
                 t_enable=True,
                 t_cap=100000,
                 verbose=0):
        """Create an instance of the agent and set initial attributes.

        Args:
            name: A string keyword argument that sets a display name for
                the agent.
            time: A float keyword argument for the time in seconds for
                the agent to pick a move.
            prune_enable: A boolean keyword argument that sets the
                pruning behavior for the agent. See the prune method.
            t_enable: A boolean keyword argument that sets the
                transposition table behavior for the agent. The agent
                will use a transposition table if this is set to True.
            t_cap: The capacity of the LRU transposition table.
            verbose: An integer keyword argument that sets the verbosity
                of the agent. The values indicate:
                - 0: No console output.
                - 1: Prints the best move and estimated score for the
                    provided gamestate at each depth level.
                - 2: Prints the best move, score, and principal
                    variation found at each depth level.
                - 3: Prints the best move, score, principal variation,
                    and time elapsed at each depth level.
                - 4: Prints as in 3 but includes pruning-related output.
                - 5: Prints as in 3 but includes pruning-related and
                    transposition table-related output.
        """
        self.name = name
        self.time = time
        self.pruning = prune_enable
        self.t_enable = t_enable
        self.t_cap = t_cap
        self._verbose = verbose

        self.reset()

    def reset(self):
        """Reset attributes to default values."""
        # Attributes for traversing the game tree.
        self._time_ini = None
        self._time_last = None
        self._turn = None
        self.complete = True
        self.depth_sum = 0
        self.move_count = 0

        # Initial transposition table.
        self.ttable = OrderedDict()

    def get_move(self, gamestate):
        """Find the best move using iterative deepening.

        Depth for the search starts at 1 and increments as far as
        possible based on allotted time.

        Args:
            gamestate: An instance of the gamestate class being played.
                Searches the game tree starting from this gamestate.

        Returns:
            An instance of the move class corresponding to the
            gamestate class being played. The chosen move is the best
            move found by the agent from the list of legal moves at the
            provided gamestate.
        """
        # Set instance attributes
        self._time_ini = time.time()
        self._time_last = time.time()
        self._turn = gamestate.turn

        # Default move is random; search should improve on this.
        saved_move = random.choice(gamestate.valid_moves)

        depth = 1
        while True:
            self.complete = True  # Tree complete until shown otherwise.
            next_kwargs = self.calc_kwargs(gamestate, None)
            score, pv = self.depth_search(gamestate, depth, **next_kwargs)

            if self._verbose in (1, 2, 3, 4, 5):
                print('----------------------')
                print(self.name)
            self.console_output(depth, score, pv)

            # None score indicates out of time; return the most
            # recently selected move.
            if score is None:
                self.depth_sum += depth - 1
                self.move_count += 1
                return saved_move

            saved_move = pv[-1]

            # If the game tree has been fully explored, no more search
            # is required.
            if self.complete is True:
                self.depth_sum += depth
                self.move_count += 1
                return saved_move

            depth += 1

    def depth_search(self, gamestate, depth, **kwargs):
        """Evaluate the current gamestate to a given depth.

        Traverses the game tree in a DFS method in a general setting.
        The behavior can be customized (e.g. for subclasses) by the
        methods prune, calc_kwargs, and _is_better.

        Args:
            gamestate: An instance of the gamestate class being played.
                The root of the tree to search.
            depth: An integer of the number of plies to search forward.

        Keyword Args:
            Uses wildcard keyword args as calculated by the calc_kwargs
            method. This allows for customizing the behavior while
            maintaining the same DFS structure.

        Returns:
            A tuple (score, pv), where score is the estimated score of
            the gamestate argument found, and pv is the principal
            variation found to reach that score. The principal variation
            is a list of move instances.
        """
        if time.time() - self._time_ini >= self.time:
            # Out of time.
            return None, None
        elif gamestate.is_game_over():
            # Terminal node; use scoring heuristic.
            return gamestate.score, []
        elif depth == 0:
            # Use scoring heuristic and note tree as incomplete.
            self.complete = False
            return gamestate.score, []
        else:
            # Order moves for optimal pruning (if enabled).
            ordered_states = self.order_moves(gamestate)

            # Initialize trackers.
            next_kwargs = self.calc_kwargs(gamestate, None, **kwargs)
            best_score, best_pv = self.depth_search(ordered_states[0][1],
                                                    depth-1,
                                                    **next_kwargs)
            if best_score is None:
                return None, None
            best_move = ordered_states[0][0]

            # Iterate through remaining moves and select the best.
            for move, next_state in ordered_states[1:]:
                if self.prune(gamestate, best_score, **kwargs):
                    break
                next_kwargs = self.calc_kwargs(gamestate, best_score, **kwargs)
                score, pv = self.depth_search(next_state,
                                              depth-1,
                                              **next_kwargs)
                if score is None:
                    return None, None
                if self._is_better(score, best_score, gamestate.turn):
                    best_score = score
                    best_move = move
                    best_pv = pv

            # Update transposition table with determined score.
            self.update_ttable(gamestate, best_score)

            # Update principal variation and return.
            best_pv.append(best_move)
            return best_score, best_pv

    def order_moves(self, gamestate):
        """Order the valid moves more optimally for pruning.

        Args:
            gamestate: An instance of the gamestate class being played.
                Orders the valid moves from this gamestate.

        Returns:
            A list of move, gamestate pairs (where the gamestate is
            obtained from the gamestate argument with the corresponding
            move). These are ordered according to some scheme to
            improve pruning performance.
        """
        return [(move, gamestate.get_next(move))
                for move in gamestate.valid_moves]

    def access_ttable(self, gamestate, turn):
        """Lookup the given gamestate in the transposition table.

        The returned score is a float, chosen from the score tuple by
        the turn argument.

        Args:
            gamestate: An instance of the Gamestate class being played.
            turn: The index of the score tuple to return.
        """
        try:
            # Attempt lookup in LRU transposition table
            self.ttable.move_to_end(gamestate.hash_value)
            return self.ttable[gamestate.hash_value][turn]
        except (AttributeError, KeyError):
            # If hash_value is not defined or it is not present in the
            # table, return an estimate for an average value.
            return gamestate.upper_sum / gamestate.players

    def prune(self, gamestate, best_score, **kwargs):
        """Decide whether to prove the current subtree.

        Args:
            gamestate: An instance of the gamestate class being played.
                Is the root node for the subtree to be pruned.
            best_score: The greatest score under the ordering in the
                _is_better method.

        Keyword Args:
            Uses wildcard keyword args. These are the bound for shallow
            pruning and the alpha, beta values for alpha-beta pruning.

        Returns:
            True or False corresponding whether to prune the tree.
        """
        return False

    def calc_kwargs(self, gamestate, best_score, **kwargs):
        """Determine the keyword args for the next depth search.

        Args:
            gamestate: An instance of the gamestate class being played.
            best_score: The greatest score found prior to this depth.

        Keyword Args:
            Uses wildcard keyword args for custom behavior.

        Returns:
            A dictionary of keyword arguments to be passed to the next
            depth_search call.
        """
        return dict()

    def _is_better(self, new_score, old_score, turn):
        """Determine which score is better.

        Args:
            new_score, old_score: scores (tuples of floats) to be
                compared by this method.
            turn:
                The turn of the gamestate under consideration; this
                indexes the score tuples.

        Returns:
            True if new_score is better than old_score, and false
            otherwise.
        """
        return False

    def tiebreak(self, new_score, old_score, turn):
        """Break ties in determining the best score Used by _is_better.

        Args:
            new_score, old_score: scores (tuples of floats) to be
                compared by thie method.
            turn:
                The turn of the gamestate under consideration; this
                indexes the score tuples.

        Returns:
            True if the new_score wins the tie, and False otherwise.
        """
        return False

    def update_ttable(self, gamestate, score):
        """Update the transposition table with the new score found.

        Args:
            gamestate: An instance of the gamestate class being played.
            score: The score estimate found for the gamestate by this
                class.
        """
        if self.t_enable and hasattr(gamestate, 'hash_value'):
            self.ttable[gamestate.hash_value] = score
            self.ttable.move_to_end(gamestate.hash_value)
            if len(self.ttable) > self.t_cap:
                self.ttable.popitem(last=False)

    def console_output(self, depth, score, pv):
        """Output data to console at each depth.

        Args:
            depth: The depth just finished by the agent.
            score: The score found at that depth.
            pv: The principal variation found at that depth.
        """
        # Basic information
        if self._verbose in (1, 2, 3, 4, 5):
            print('----------------------')
            print('Depth {}'.format(depth))
            if score is None:
                print('Ran out of time.')
            else:
                print('Best move: {}'.format(pv[-1]))
                print('Score: {}'.format(score))
            if self.complete:
                print('Tree complete.')
            else:
                print('Tree Incomplete.')
            if self.move_count == 0:
                average_depth = depth
            else:
                average_depth = self.depth_sum / self.move_count
            print('Average depth finished: {}'.format(average_depth))

        # Principal variation
        if self._verbose in (2, 3, 4, 5) and score is not None:
            print('Principal variation:')
            print([str(move) for move in pv[::-1]])

        # Timing
        if self._verbose in (3, 4, 5):
            print('Time Elapsed:')
            print('This depth: {}'.format(time.time() - self._time_last))
            self._time_last = time.time()
            print('Total: {}'.format(time.time() - self._time_ini))

        # Transposition Table
        if self._verbose in (5,):
            if self.t_enable:
                print('Transposition table: ({}/{})'.format(len(self.ttable),
                                                            self.t_cap))
            else:
                print('Transposition table disabled.')

        if self._verbose in (1, 2, 3, 4, 5):
            print('----------------------\n')


class MaxnAgent(IDDFSAgent):
    """An agent using the Max^n algorithm with iterative deepening.

    Subclasses the IDDFSAgent base class, and determines the best move
    by assuming each player will seek to maximize their own score.
    """

    def __init__(self,
                 name='Maxn Agent',
                 time=30.0,
                 prune_enable=True,
                 t_enable=True,
                 t_cap=100000,
                 verbose=0):
        """See base class documentation."""
        super().__init__(name=name,
                         time=time,
                         prune_enable=prune_enable,
                         t_enable=t_enable,
                         t_cap=t_cap,
                         verbose=verbose)

    def order_moves(self, gamestate):
        """Order moves by highest score at given gamestate.

        See base class for parameter and return documentation.
        """
        next_list = [(move, gamestate.get_next(move))
                     for move in gamestate.valid_moves]
        return sorted(next_list,
                      key=(lambda next_tup:
                           self.access_ttable(next_tup[1], gamestate.turn)),
                      reverse=True)

    def prune(self, gamestate, best_score, **kwargs):
        """Prune the game tree using shallow pruning.

        Deep pruning is not consistent using the Maxn algorithm.
        Instead, shallow pruning is optimal.

        See base class for parameter and return documentation.
        """
        if not self.pruning:
            return False
        if best_score[gamestate.turn] >= kwargs['bound']:
            if self._verbose in (4, 5):
                print('Shallow pruned with score {}'.format(best_score))
            return True
        return False

    def calc_kwargs(self, gamestate, best_score, **kwargs):
        """Calculate the next bound for shallow pruning.

        See base class for parameter and return documentation.
        """
        if best_score is None:
            best_score = (gamestate.lower,) * gamestate.players
        correction = -(gamestate.players - 2) * gamestate.lower
        return {'bound': (gamestate.upper_sum
                          - best_score[gamestate.turn]
                          + correction)}

    def _is_better(self, new_score, old_score, turn):
        """Determime the best score using the maxn algorithm.

        See base class for parameter and return documenttion.
        """
        if new_score[turn] > old_score[turn]:
            return True
        elif new_score[turn] == old_score[turn]:
            return self.tiebreak(new_score, old_score, turn)
        return False

    def tiebreak(self, new_score, old_score, turn):
        """Break ties with paranoid assumption, then randomly.

        See base class for parameter and return documentation.
        """
        if new_score[self._turn] < old_score[self._turn]:
            return True
        else:
            return random.choice((True, False))


class ParanoidAgent(IDDFSAgent):
    """An agent using the paranoid algorithm with iterative deepening.

    Transforms any game to a 2-player zero-sum game by assuming that
    all other players are attempting to minimize the agent's score,
    with no regard for their own score. This assumption may not be
    accurate but allows for alpha-beta pruning and a simpler score.
    """

    def __init__(self,
                 name='Paranoid Agent',
                 time=30.0,
                 prune_enable=True,
                 t_enable=True,
                 t_cap=100000,
                 verbose=0):
        """See base class documentation."""
        super().__init__(name=name,
                         time=time,
                         prune_enable=prune_enable,
                         t_enable=t_enable,
                         t_cap=t_cap,
                         verbose=verbose)

    def order_moves(self, gamestate):
        """Order moves by highest or lowest root score.

        See base class for parameter and return documentation.
        """
        next_list = [(move, gamestate.get_next(move))
                     for move in gamestate.valid_moves]
        return sorted(next_list,
                      key=(lambda next_tup:
                           self.access_ttable(next_tup[1], self._turn)),
                      reverse=(gamestate.turn == self._turn))

    def prune(self, gamestate, best_score, **kwargs):
        """Prune the game tree using alpha-beta pruning.

        See base class for parameter and return documentation.
        """
        if not self.pruning:
            return False
        if (gamestate.turn == self._turn
                and best_score[self._turn] > kwargs['beta']):
            return True
        elif best_score[self._turn] < kwargs['alpha']:
            return True
        return False

    def calc_kwargs(self, gamestate, best_score, **kwargs):
        """Calculate next alpha and beta values.

        See base class for parameter and return documentation.
        """
        if not kwargs:
            # Initialize alpha, beta
            return {'alpha': float('-inf'),
                    'beta': float('inf')}
        if best_score is None:
            return {'alpha': kwargs['alpha'],
                    'beta': kwargs['beta']}
        if gamestate.turn == self._turn:
            return {'alpha': max(kwargs['alpha'], best_score[self._turn]),
                    'beta': kwargs['beta']}
        else:
            return {'alpha': kwargs['alpha'],
                    'beta': min(kwargs['beta'], best_score[self._turn])}

    def _is_better(self, new_score, old_score, turn):
        """Determine which score is better using the paranoid algorithm.

        See base class for parameter and return documentation.
        """
        if new_score[self._turn] == old_score[self._turn]:
            return self.tiebreak(new_score, old_score, turn)
        elif (turn == self._turn
              ^ (new_score[self._turn] < old_score[self._turn])):
            return True
        return False

    def tiebreak(self, new_score, old_score, turn):
        """Break ties randomly.

        See base class for parameter and return documentation.
        """
        return random.choice((True, False))
