import random
from gabasic import ToolboxContributor
from tictactoe import TicTacToeChromo, PolicyGene


class ChangeActionMutation(ToolboxContributor):
  def __init__(self, **kwargs):
    super(ChangeActionMutation, self).__init__()
    self.indiv_gene_mut_prob = float(kwargs.get('indiv_gene_mut_prob', '0.05'))

  def __call__(self, individual):
    if not isinstance(individual, dict):
      raise TypeError(
        'ChangeActionMutation requires a dict individual'
      )
    for a_value in individual.values():
      if random.random() <= self.indiv_gene_mut_prob:
        board_state = PolicyGene.state_domain.rank_idx_pair_to_state(
          a_value.state_tuple
        )
        new_action = random.choice(board_state.legal_moves())
        a_value.action = new_action
    return (individual,)

  def configure_toolbox(self, toolbox):
    toolbox.register('mutate', self)

# vim: set ts=2 sw=2 expandtab:
