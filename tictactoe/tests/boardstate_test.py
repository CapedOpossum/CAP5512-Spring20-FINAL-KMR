import unittest
import itertools
from tictactoe import BoardState, BoardStateDomain


class BoardStateTestCase(unittest.TestCase):
  def test_basic_equality(self):
    first_state = BoardState([1,0,0,2,0,0,0,0,0])
    second_state = BoardState([1,0,0,2,0,0,0,0,0])
    self.assertEqual(first_state, second_state)

  def test_alternate_equality(self):
    # 1 0 0
    # 2 0 0
    # 0 0 0
    baseline_state = BoardState([1,0,0,2,0,0,0,0,0])
    alt_states = []
    # 0 0 0
    # 0 0 0
    # 1 2 0
    alt_states.append(BoardState([0, 0, 0, 0, 0, 0, 1, 2, 0]))
    # 0 0 0
    # 0 0 2
    # 0 0 1
    alt_states.append(BoardState([0, 0, 0, 0, 0, 2, 0, 0, 1]))
    # 0 2 1
    # 0 0 0
    # 0 0 0
    alt_states.append(BoardState([0, 2, 1, 0, 0, 0, 0, 0, 0]))
    # 0 0 1
    # 0 0 2
    # 0 0 0
    alt_states.append(BoardState([0, 0, 1, 0, 0, 2, 0, 0, 0]))
    # 0 0 0
    # 2 0 0
    # 1 0 0
    alt_states.append(BoardState([0, 0, 0, 2, 0, 0, 1, 0, 0]))
    # 0 0 0
    # 0 0 0
    # 0 2 1
    alt_states.append(BoardState([0, 0, 0, 0, 0, 0, 0, 2, 1]))
    # 1 2 0
    # 0 0 0
    # 0 0 0
    alt_states.append(BoardState([1, 2, 0, 0, 0, 0, 0, 0, 0]))
    for an_alt in alt_states:
      self.assertEqual(baseline_state, an_alt)

  def test_basic_inequality(self):
    baseline_state = BoardState([1, 0, 0, 2, 0, 0, 0, 0, 0])
    other_state = BoardState([1, 0, 0, 0, 2, 0, 0, 0, 0])
    self.assertNotEqual(baseline_state, other_state)

  def test_rank_properties(self):
    ranks = []
    ranks.append(BoardState([1, 0, 0, 0, 0, 0, 0, 0, 0]))
    ranks.append(BoardState([1, 2, 0, 0, 0, 0, 0, 0, 0]))
    ranks.append(BoardState([1, 2, 1, 0, 0, 0, 0, 0, 0]))
    ranks.append(BoardState([1, 2, 1, 2, 0, 0, 0, 0, 0]))
    ranks.append(BoardState([1, 2, 1, 2, 0, 0, 1, 0, 0]))
    ranks.append(BoardState([1, 2, 1, 2, 0, 0, 1, 0, 2]))
    ranks.append(BoardState([1, 2, 1, 2, 0, 1, 1, 0, 2]))
    ranks.append(BoardState([1, 2, 1, 2, 2, 1, 1, 0, 2]))
    ranks.append(BoardState([1, 2, 1, 2, 2, 1, 1, 2, 2]))
    self.assertEqual(1, ranks[0].rank)
    self.assertEqual(2, ranks[1].rank)
    self.assertEqual(3, ranks[2].rank)
    self.assertEqual(4, ranks[3].rank)
    self.assertEqual(5, ranks[4].rank)
    self.assertEqual(6, ranks[5].rank)
    self.assertEqual(7, ranks[6].rank)
    self.assertEqual(8, ranks[7].rank)
    self.assertEqual(9, ranks[8].rank)
    for uut_idx in range(len(ranks)):
      uut = ranks[uut_idx]
      oppos = []
      oppos.extend(ranks)
      del oppos[uut_idx]
      for an_oppo in oppos:
        self.assertNotEqual(uut, an_oppo)

  def test_victory(self):
    p1_victories = [
      BoardState([1, 1, 1, 2, 2, 1, 2, 1, 0]), # Across
      BoardState([2, 2, 1, 1, 1, 1, 2, 1, 0]), # Across
      BoardState([2, 1, 2, 2, 1, 0, 1, 1, 1]), # Across
      BoardState([1, 0, 2, 1, 2, 0, 1, 0, 0]), # Down
      BoardState([2, 1, 2, 0, 1, 0, 0, 1, 0]), # Down
      BoardState([0, 0, 1, 0, 2, 1, 2, 0, 1]), # Down
      BoardState([1, 0, 2, 0, 1, 2, 0, 0, 1]), # Diag high-low
      BoardState([2, 0, 1, 2, 1, 0, 1, 0, 0]), # Diag low-high
    ]
    p2_victories = [
      BoardState([2, 2, 2, 1, 1, 2, 1, 2, 0]), # Across
      BoardState([1, 1, 2, 2, 2, 2, 1, 2, 0]), # Across
      BoardState([1, 2, 1, 1, 2, 0, 2, 2, 2]), # Across
      BoardState([2, 0, 1, 2, 1, 0, 2, 0, 0]), # Down
      BoardState([1, 2, 1, 0, 2, 0, 0, 2, 0]), # Down
      BoardState([0, 0, 2, 0, 1, 2, 1, 0, 2]), # Down
      BoardState([2, 0, 1, 0, 2, 1, 0, 0, 2]), # Diag high-low
      BoardState([1, 0, 2, 1, 2, 0, 2, 0, 0]), # Diag low-high
    ]
    for a_p1_vic in p1_victories:
      self.assertEqual((True, False), a_p1_vic.player_victory)
    for a_p2_vic in p2_victories:
      self.assertEqual((False, True), a_p2_vic.player_victory)

  def test_stalemate(self):
    stalemates = [
      BoardState([1, 2, 1, 1, 2, 1, 2, 1, 2]),
      BoardState([1, 1, 2, 2, 2, 1, 1, 2, 1])
    ]

    for a_stalemate in stalemates:
      self.assertTrue(a_stalemate.full)
      self.assertEqual((False, False), a_stalemate.player_victory)

  def test_legal_moves(self):
    cases = [
      BoardState([0, 0, 1, 0, 2, 2, 1, 1, 2]),
      BoardState([1, 2, 1, 2, 0, 0, 0, 0, 0])
    ]
    expected_results = [
      [0, 1, 3],
      [4, 5, 6, 7, 8]
    ]
    for a_case, expectation in zip(cases, expected_results):
      self.assertEqual(expectation, a_case.legal_moves())

class BoardStateDomainTestCase(unittest.TestCase):
  def test_discovery_from_empty(self):
    uut = BoardStateDomain()
    new_state = BoardState([1, 0, 0, 0, 0, 0, 0, 0, 0])
    (rank, idx) = uut.state_to_rank_idx_pair(new_state)
    self.assertEqual(1, rank)
    self.assertEqual(0, idx)

  def test_domain_addr_consistency(self):
    rank_2_0 = BoardState([1, 0, 0, 2, 0, 0, 0, 0, 0])
    rank_2_0_alt = BoardState([0, 0, 0, 0, 0, 0, 1, 2, 0])
    rank_2_1 = BoardState([1, 0, 0, 0, 2, 0, 0, 0, 0])
    rank_3_0 = BoardState([1, 2, 1, 0, 0, 0, 0, 0, 0])
    uut = BoardStateDomain()
    self.assertEqual((2, 0), uut.state_to_rank_idx_pair(rank_2_0))
    self.assertEqual((2, 1), uut.state_to_rank_idx_pair(rank_2_1))
    self.assertEqual((3, 0), uut.state_to_rank_idx_pair(rank_3_0))
    self.assertEqual((2, 0), uut.state_to_rank_idx_pair(rank_2_0_alt))
    self.assertEqual(rank_2_0, uut.rank_idx_pair_to_state((2, 0)))
    self.assertEqual(rank_2_0_alt, uut.rank_idx_pair_to_state((2, 0)))
    self.assertEqual(rank_2_1, uut.rank_idx_pair_to_state((2, 1)))
    self.assertEqual(rank_3_0, uut.rank_idx_pair_to_state((3, 0)))

if __name__ == '__main__':
  unittest.main()

# vim: set ts=2 sw=2 expandtab:
