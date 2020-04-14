import random
from gabasic import ToolboxContributor
from . import BoardState, PolicyGene


class WinsVsLosses(ToolboxContributor):
  def __init__(self, **kwargs):
    super(WinsVsLosses, self).__init__()
  
  def configure_toolbox(self, toolbox):
    toolbox.register('evaluate', self)
  
  def __call__(self, individual):
    result = self.player_first(individual)
    result += self.opponent_first(individual)
    return (result,)

  def _traverse_tree(self, individual, fringe):
    """Execute depth-first traversal of board state tree, scoring based on leaf
    nodes.

    Traversal requires a pre-initialized exploration "fringe". The way this
    fringe is initialized determines which player went first.

    Player only gets one move possibility based on either the existing policy or
    a random move.

    Opponent is able to execute all possible moves for a particular board state.
    """
    result = 0
    while fringe:
      board_state = fringe.pop()
      if board_state.final:
        # Victory: +1 score
        # Defeat: -1 score
        # Draw: no change in score
        if board_state.player_victory[0]:
          result += 1
        elif board_state.player_victory[1]:
          result -= 1
        continue
      # Our move
      state_addr = PolicyGene.state_domain.state_to_rank_idx_pair(board_state)
      board_state = PolicyGene.state_domain.rank_idx_pair_to_state(state_addr)
      if state_addr not in individual:
        individual[state_addr] = PolicyGene(
          state_addr,
          random.choice(board_state.legal_moves())
        )
      board_state = board_state.after_move(1, individual[state_addr].action)
      # Opponent move
      if not board_state.final:
        state_addr = PolicyGene.state_domain.state_to_rank_idx_pair(board_state)
        board_state = PolicyGene.state_domain.rank_idx_pair_to_state(state_addr)
        fringe.extend(
          [
            board_state.after_move(2, a_move)
            for a_move in board_state.legal_moves()
          ]
        )
    return result

  def opponent_first(self, individual):
    initial_state = BoardState([0, 0, 0, 0, 0, 0, 0, 0, 0])
    fringe = [
      initial_state.after_move(2, a_move)
      for a_move in initial_state.legal_moves()
    ]
    return self._traverse_tree(individual, fringe)

  def player_first(self, individual):
    fringe = [BoardState([0, 0, 0, 0, 0, 0, 0, 0, 0]),]
    return self._traverse_tree(individual, fringe)

# vim: set ts=2 sw=2 expandtab:
