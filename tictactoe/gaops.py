import random
from gabasic import ToolboxContributor
from tictactoe import TicTacToeChromo, PolicyGene


class ChangeActionMutation(ToolboxContributor):
  def __init__(self, **kwargs):
    super(ChangeActionMutation, self).__init__()
    self.indiv_gene_mut_rate = float(kwargs.get('indiv_gene_mut_rate', '0.05'))

  def do_mutation(self, individual):
    if not isinstance(individual, TicTacToeChromo):
      raise TypeError(
        'ChangeActionMutation requires a TicTacToeChromo individual'
      )
    for a_value in individual.values():
      if random.random() <= self.indiv_gene_mut_rate:
        board_state = PolicyGene.state_domain.rank_idx_pair_to_state(
          a_value.state_tuple
        )
        new_action = random.choice(board_state.legal_actions())
        a_value.action = new_action

  def configure_toolbox(self, toolbox):
    toolbox.register('mutate', self.do_mutation)

# vim: set ts=2 sw=2 expandtab:
