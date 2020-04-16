# pylint: disable=no-member

import types
import random
from deap import tools, creator
from gabasic import ToolboxContributor
from . import BoardState, BoardStateDomain


class PolicyGene(object):
  """Represents an individual, indivisible element that makes up an entire
  chromosome in Tic-Tac-Toe.

  A gene is made up of a state tuple which can be resolved, using a
  py:class::BoardStateDomain, into a fully-specified Tic-Tac-Toe board state.
  The gene also contains an action which should be taken whenever the
  Tic-Tac-Toe board is at the state represented by the state tuple.

  Attributes
  ----------
  state_tuple : tuple
    Tuple that represents the board state; must be resolved using the
    py:class::BoardStateDomain instance assigned to the class.
  action : int
    Action that must be taken whenever the board state is as shown by the
    ``state_tuple`` attribute.
  
  codeauthor:: Rolando J. Nieves <rolando.j.nieves@knights.ucf.edu>
  """

  state_domain = None

  def __init__(self, state_tuple, action):
    """Initialize the gene instance with the information provided.

    Parameters
    ----------
    state_tuple : tuple
      Tuple that represents this gene's board state.
    action : int
      Action that should be taken when the board is in the gene's corresponding
      state.
    """
    super(PolicyGene, self).__init__()
    self.state_tuple = state_tuple
    self.action = action
  
  @classmethod
  def new_random(cls):
    """Create a new py:class:: PolicyGene instance with randomly-generated
    values.

    Despite the fact that the gene information is randomly-generated, care is
    taken so that it is a valid state-action pair.

    Returns
    -------
    PolicyGene
      New randomly-generated py:class::PolicyGene instance.
    
    Raises
    ------
    RuntimeError
      If the ``state_domain`` class attribute has not been previously
      initialized.
    """
    if cls.state_domain is None:
      raise RuntimeError('State domain not initialized.')

    found = False

    while not found:
      target_rank = random.randint(0, 8)
      next_player = 1
      board_state = BoardState([0, 0, 0, 0, 0, 0, 0, 0, 0])

      while target_rank > 0:
        legal_moves = board_state.legal_moves()
        next_move = random.choice(legal_moves)
        board_state = board_state.after_move(next_player, next_move)
        next_player = 2 if next_player == 1 else 1
        target_rank -= 1

      found = not board_state.final

    # Register board state that we are happy with
    state_tuple = cls.state_domain.state_to_rank_idx_pair(board_state)

    # Read it back from the domain just in case we came up with a variation of
    # one that was already present.
    board_state = cls.state_domain.rank_idx_pair_to_state(state_tuple)

    # Select a valid action at random from the board state
    action = random.choice(board_state.legal_moves())

    return PolicyGene(state_tuple, action)

  def __str__(self):
    return '{state_tuple:}: {action:}'.format(**vars(self))

class TicTacToeChromo(ToolboxContributor):
  """Represents a GA individual that encodes a Tic-Tac-Toe policy.

  The internal storage of this class' instances is a dictionary that uses the
  py:class:: PolicyGene ``state_tuple`` field as the key. Doing so ensures that
  these chromosomes will never contain more than one action for each board
  state.

  codeauthor:: Rolando J. Nieves <rolando.j.nieves@knights.ucf.edu>
  """

  @staticmethod
  def from_generator(generator=None):
    """Initialize the chromosome information, using a generator if provided.

    Parameters
    ----------
    generator : types.GeneratorType or None
      If provided, the generator that will be used to populate the gene.
    """
    result = creator.PlayerPolicy()

    if generator is not None and isinstance(generator, types.GeneratorType):
      for a_gene in generator:
        if isinstance(a_gene, PolicyGene):
          result[a_gene.state_tuple] = a_gene

    return result

  def __init__(self, fitness_type, **kwargs):
    super(TicTacToeChromo, self).__init__()
    fitness = creator.__dict__[fitness_type]
    creator.create(
      'PlayerPolicy',
      dict,
      fitness=fitness
    )
    self.init_policy_slot_count = int(
      kwargs.get('init_policy_slot_count', '20')
    )
    PolicyGene.state_domain = BoardStateDomain()

  def configure_toolbox(self, toolbox):
    toolbox.register(
      'individual',
      tools.initRepeat,
      TicTacToeChromo.from_generator,
      PolicyGene.new_random,
      n=self.init_policy_slot_count
    )
    toolbox.register(
      'population',
      tools.initRepeat,
      list,
      toolbox.individual
    )

# vim: set ts=2 sw=2 expandtab:

