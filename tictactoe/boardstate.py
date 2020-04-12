import numpy as np


class BoardState(object):
  """Immutable state of the Tic-Tac-Toe board.

  Instances of this class represent a particular tic-tac-toe board state, and
  the state is considered equivalent with seven (7) other rotations and
  reflexions of the baseline configuration.

  Instances can also be used to create new board states after making a
  particular move for a player. Since instances are immutable, a new instance
  is created after the move is made.

  Moves expressed in terms of the state's baseline configuration can also be
  translated to moves in the other equivalent configurations.

  Board states are also assigned a "rank" based on the number of moves that
  the state expresses. The rank range is [0, 9] with 0 being an empty board, 9
  being a full board, and the rest distributed between.

  Attributes
  ----------
  rank : int
    Read-only attribute that indicates the rank of this board state.

  codeauthor:: Rolando J. Nieves <rolando.j.nieves@knights.ucf.edu>
  """
  # TODO: Could these be derived using an algorithm? That would make this class
  # truly generic, as it would not depend on just a 3 x 3 board.
  # For any board described by configuration:
  #
  # 0 1 2
  # 3 4 5
  # 6 7 8
  #
  # Configurations that may be considered equivalent are:
  # 2 5 8    8 7 6    6 3 0    2 1 0    6 7 8    8 5 2    0 3 6
  # 1 4 7    5 4 3    7 4 1    5 4 3    3 4 5    7 4 1    1 4 7
  # 0 3 6    2 1 0    8 5 2    8 7 6    0 1 2    6 3 0    2 5 8
  CONFIG_SCHEMAS = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [2, 5, 8, 1, 4, 7, 0, 3, 6],
    [8, 7, 6, 5, 4, 3, 2, 1, 0],
    [6, 3, 0, 7, 4, 1, 8, 5, 2],
    [2, 1, 0, 5, 4, 3, 8, 7, 6],
    [6, 7, 8, 3, 4, 5, 0, 1, 2],
    [8, 5, 2, 7, 4, 1, 6, 3, 0],
    [0, 3, 6, 1, 4, 7, 2, 5, 8]
  ]

  def __init__(self, contents):
    """Save the provided baseline configuration, deriving alternates and rank.

    Parameters
    ----------
    contents : list
      Board contents that will be considered as the baseline configuration.
    """
    super(BoardState, self).__init__()
    self._baseline = contents
    self._all_configs = [self._baseline,]
    for a_config in BoardState.CONFIG_SCHEMAS[1:]:
      self._all_configs.append([0] * len(a_config))
      for target_pos, source_idx in enumerate(a_config):
        self._all_configs[-1][target_pos] = self._baseline[source_idx]
    self._rank = len(BoardState.CONFIG_SCHEMAS[0]) - self._baseline.count(0)
    self._max_move = max(BoardState.CONFIG_SCHEMAS[0])
    # Assuming board is always a square with n cells, dimensions should be
    # sqrt(n) by sqrt(n)
    a_dim = int(np.sqrt(len(BoardState.CONFIG_SCHEMAS[0])))
    board_shape = (a_dim, a_dim)
    square_board = np.reshape(np.array(self._baseline), board_shape)
    p1_moves = square_board == 1
    p2_moves = square_board == 2
    d1_mask = np.eye(a_dim, dtype=int) == 0
    d2_mask = np.fliplr(np.eye(a_dim, dtype=int)) == 0
    p1_d1_masked = np.ma.array(p1_moves, mask=d1_mask, copy=True)
    p1_d2_masked = np.ma.array(p1_moves, mask=d2_mask, copy=True)
    p2_d1_masked = np.ma.array(p2_moves, mask=d1_mask, copy=True)
    p2_d2_masked = np.ma.array(p2_moves, mask=d2_mask, copy=True)
    (self._p1_victory, self._p2_victory) = (
      np.any(np.all(p1_moves, axis=1)) or  # Across
      np.any(np.all(p1_moves, axis=0)) or  # Down
      np.all(p1_d1_masked) or              # Diagonal high-low
      np.all(p1_d2_masked),                # Diagonal low-high
      np.any(np.all(p2_moves, axis=1)) or  # Across
      np.any(np.all(p2_moves, axis=0)) or  # Down
      np.all(p2_d1_masked) or              # Diagonal high-low
      np.all(p2_d2_masked)                 # Diagonal low-high
    )
  
  def legal_moves(self):
    """Discover moves left in board state

    Returns
    -------
    list
      Remaining moves in this board state. Could be empty if board is full.
    """
    result = []
    for (idx, pos) in enumerate(self._baseline):
      if pos == 0:
        result.append(idx)
    return result
  
  @property
  def rank(self):
    """Provide read-only access to board state rank.

    Returns
    -------
    int
      Rank of this board state in range [0, 9]
    """
    return self._rank

  def after_move(self, player, move):
    """Create new board state resulting after a player move.

    Since BoardState instances are immutable, a new instance must be created
    after a player move is applied.

    Given that the resulting board state will be of higher rank, there is no
    chance that the result of this method will be an equivalent configuration
    of the current board state.

    Parameters
    ----------
    player : int
      Identity of player moving in the range [1, 2]
    move : int
      Move to apply on the baseline board state in range [0, 8]
    
    Returns
    -------
    BoardState
      New instance reflecting the player move.
    """
    if self._baseline[move] != 0:
      raise ValueError(
        'Move ({}) illegal on board [{}]'.format(move, self._baseline)
      )
    new_baseline = []
    new_baseline.extend(self._baseline)
    new_baseline[move] = player
    return BoardState(new_baseline)

  def adjust_move_to_config(self, baseline_move, config_idx):
    """Translate a board move based on a particular equivalent configuration.

    All moves in this class are considered based on the baseline configuration.
    If a move is to be applied to a board with an equivalent but alternate
    configuration, it must be translated using this facility.

    Parameters
    ----------
    baseline_move : int
      Move to be translated in the range [0, 8]
    config_idx : int
      Index of the configuration to translate the move into, with 0 being the
      baseline configuration and the range [1, 7] being the alternates.
    """
    if baseline_move < 0 or baseline_move > self._max_move:
      raise ValueError('Invalid move ({})'.format(baseline_move))
    if config_idx < 0 or config_idx > len(BoardState.CONFIG_SCHEMAS):
      raise ValueError('Invalid configuration index({})'.format(config_idx))
    return BoardState.CONFIG_SCHEMAS[config_idx][baseline_move]

  def matching_config(self, other):
    """Obtain the index of the configuration that matches the other BoardState
    instance.

    Parameters
    ----------
    other : BoardState
      Instance to be evaluated.
    
    Returns
    -------
    int
      Index of the configuration that matches ``other``; ``-1`` if no
      configuration matches (i.e., the board states are not equivalent).
    """
    result = -1
    config_count = len(self._all_configs)
    config_idx = 0
    while result == -1 and config_idx < config_count:
      if other._baseline == self._all_configs[config_idx]:
        result = config_idx
      config_idx += 1
    return result

  def __eq__(self, other):
    """Test another object instance for equality with this one.

    Two instances are equal if they are of the same type and their board state
    configurations are equivalent based on the rotation and reflection 
    alternates.

    Parameters
    ----------
    other
      Instance to be evaluated
    
    Returns
    -------
    bool
      ``True`` if ``other`` is equivalent to this instance; ``False`` otherwise.
    """
    return isinstance(other, BoardState) and self.matching_config(other) != -1

  def __str__(self):
    """Express baseline state as a string-encoded array.

    Returns
    -------
    str
      Baseline state as a string-encoded array.
    """
    return '{}'.format(self._baseline)

  @property
  def final(self):
    """Express whether this board state represents a final state.

    A final state is one where there's a winner or the board is full.

    Returns
    -------
    bool
      ``True`` if this state is a final state; ``False`` otherwise.
    """
    return np.any(self.player_victory) or self.full

  @property
  def full(self):
    """Show whether this state represents a full board.

    Returns
    -------
    bool
      ``True`` if this state represents a full board; ``False`` otherwise.
    """
    return self._rank == len(BoardState.CONFIG_SCHEMAS[0])
  
  @property
  def player_victory(self):
    """Express whether this state represents a win for either player.

    Returns
    -------
    tuple[bool]
      First element shows whether Player 1 is victorious; second element shows
      whether the second player is victorious. For each ``True`` means victory.
    """
    return (self._p1_victory, self._p2_victory)

class BoardStateDomain(object):
  """Domain of all known board state instances.

  The primary purpose of this class is to maintain a record of all as-yet known
  py:class:: BoardState instances. All known instances, and their corresponding
  equivalents, are assigned an address that takes the form of a tuple, with the
  first tuple member being the state rank, and the second being a unique index
  within that rank.

  codeauthor:: Rolando J. Nieves <rolando.j.nieves@knights.ucf.edu>
  """
  def __init__(self):
    """Initialize storage for the known py:class:: BoardState instances
    """
    self._rank_map = {}
    self._known_state_count = 0
  def state_to_rank_idx_pair(self, board_state):
    """Obtain the corresponding domain address for a board state, creating a
    new one if necessary.

    Parameters
    ----------
    board_state : BoardState
      Instance to translate and/or register with the domain.
    
    Returns
    -------
    tuple
      Address containing rank and index.
    """
    rank_branch = []
    if board_state.rank in self._rank_map:
      rank_branch = self._rank_map[board_state.rank]
    else:
      self._rank_map[board_state.rank] = rank_branch
    try:
      branch_idx = rank_branch.index(board_state)
    except ValueError:
      branch_idx = len(rank_branch)
      rank_branch.append(board_state)
      self._known_state_count += 1
    return (board_state.rank, branch_idx)

  def rank_idx_pair_to_state(self, rank_idx_pair):
    """Obtain the py:class:: BoardState instance assigned the given address.

    Parameters
    ----------
    rank_idx_pair : tuple
      Address to de-reference within domain storage.
    
    Returns
    -------
    BoardState
      Instance assigned to the given address.
    
    Raises
    ------
    ValueError
      If the provided address is unknown to the domain.
    """
    (rank, branch_idx) = rank_idx_pair
    if not rank in self._rank_map:
      raise ValueError('Rank {} is as yet unknown.'.format(rank))
    rank_branch = self._rank_map[rank]
    if branch_idx >= len(rank_branch):
      raise ValueError(
        'Index {} in rank {} is as yet unknown.'.format(branch_idx, rank)
      )
    return rank_branch[branch_idx]

  @property
  def known_state_count(self):
    """Number of known states in the domain at the time of the call.

    Returns
    -------
    int
      Number of known states.
    """
    return self._known_state_count

# vim: set ts=2 sw=2 expandtab:
