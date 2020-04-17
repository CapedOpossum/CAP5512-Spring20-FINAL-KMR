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

  def _traverse_tree(self, individual, fringe, first):
    """Execute depth-first traversal of board state tree, scoring based on leaf
    nodes.

    Traversal requires a pre-initialized exploration "fringe". The way this
    fringe is initialized determines which player went first.

    Player only gets one move possibility based on either the existing policy or
    a random move.

    Opponent is able to execute all possible moves for a particular board state.
    """
    result = 0
    lost = 0
    total = 1

    while fringe:
      board_state = fringe.pop()

      # Point based evaluation going first
      # if board_state.final and first:
      #   # Victory: +10 score
      #   # Defeat: 0 score
      #   # Draw: +5 score
      #   if board_state.player_victory[0]:
      #     result += 10
      #   elif board_state.player_victory[1]:
      #     result += 0
      #   else:
      #     result += 5

      #   continue
      # # Point based evaluation going second
      # elif board_state.final:
      #   # Victory: +15 score
      #   # Defeat: 0 score
      #   # Draw: +10 score
      #   if board_state.player_victory[0]:
      #     result += 15
      #   elif board_state.player_victory[1]:
      #     result += 0
      #   else:
      #     result += 10

      #   continue 
      # Precentage based evalutation
      if board_state.final:
        if board_state.player_victory[0]:
          result = (total - lost) / total
        elif board_state.player_victory[1]:
          lost += 1
          result = (total - lost) / total

        total += 1
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
    return self._traverse_tree(individual, fringe, False)

  def player_first(self, individual):
    fringe = [BoardState([0, 0, 0, 0, 0, 0, 0, 0, 0]),]
    return self._traverse_tree(individual, fringe, True)

# vim: set ts=2 sw=2 expandtab:
