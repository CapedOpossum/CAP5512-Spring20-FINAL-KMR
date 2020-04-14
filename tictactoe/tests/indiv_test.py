# pylint: disable=no-member

import unittest
import random
from deap import base, tools, creator
from tictactoe import PolicyGene, BoardStateDomain, TicTacToeChromo


class PolicyGeneTest(unittest.TestCase):
  def test_to_string(self):
    uut = PolicyGene((2, 1), 2)
    self.assertEqual('(2, 1): 2', str(uut))

  def test_missing_domain_error(self):
    with self.assertRaises(RuntimeError):
      PolicyGene.new_random()

  def test_new_random(self):
    random.seed(2048)
    # All expected values obtained empirically after fixing random seed
    PolicyGene.state_domain = BoardStateDomain()
    uut = PolicyGene.new_random()
    self.assertEqual('(4, 0): 2', str(uut))
    board_state = PolicyGene.state_domain.rank_idx_pair_to_state(
      uut.state_tuple
    )
    self.assertEqual('[0, 0, 0, 0, 2, 1, 2, 1, 0]', str(board_state))

  def test_random_gen(self):
    PolicyGene.state_domain = BoardStateDomain()
    for _ in range(100):
      uut = PolicyGene.new_random()
      board_state = PolicyGene.state_domain.rank_idx_pair_to_state(
        uut.state_tuple
      )
      self.assertFalse(board_state.final)

class TicTacToeChromoTest(unittest.TestCase):
  def setUp(self):
    random.seed(2048)
    PolicyGene.state_domain = BoardStateDomain()

  def test_toolbox_gen(self):
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    toolbox = base.Toolbox()
    uut = TicTacToeChromo('FitnessMax')
    uut.configure_toolbox(toolbox)
    indiv = toolbox.individual()
    self.assertTrue(
      isinstance(indiv, dict),
      'Expected indiv to be dict but instead is "{:s}"'.format(
        indiv.__class__.__name__
      )
    )
    self.assertEqual(PolicyGene.state_domain.known_state_count, len(indiv))
    del creator.FitnessMax

  def test_toolbox_pop_gen(self):
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    toolbox = base.Toolbox()
    uut = TicTacToeChromo('FitnessMax')
    uut.configure_toolbox(toolbox)
    ga_population = toolbox.population(n=100)
    self.assertEqual(100, len(ga_population))
    for an_indiv in ga_population:
      self.assertTrue(isinstance(an_indiv, dict))
      for state_tuple, policy_gene in an_indiv.items():
        board_state = PolicyGene.state_domain.rank_idx_pair_to_state(
          state_tuple
        )
        self.assertFalse(board_state.final)
        board_state = board_state.after_move(1, policy_gene.action)
    del creator.FitnessMax

# vim: set ts=2 sw=2 expandtab:
