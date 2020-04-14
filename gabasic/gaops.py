import collections
from deap import tools
from . import ToolboxContributor

class TwoPointCrossover(ToolboxContributor):
  def __init__(self, **kwargs):
    super(TwoPointCrossover, self).__init__()
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'mate',
      tools.cxTwoPoint
    )

class OnePointMappingCrossover(ToolboxContributor):
  @staticmethod
  def mapping_keys_to_tuples(id, mapping):
    return [(id, a_key) for a_key in mapping.keys()]

  @staticmethod
  def mapping_deep_copy(src_mapping):
    result = {}
    result.update(src_mapping)
    return result

  @staticmethod
  def blend_mappings_using_tuples(src_map_1, src_map_2, keys_1, keys_2):
    src_1_copy = OnePointMappingCrossover.mapping_deep_copy(src_map_1)
    src_2_copy = OnePointMappingCrossover.mapping_deep_copy(src_map_2)
    src_map_1.clear()
    src_map_2.clear()
    for a_mapping, a_key_list in zip([src_map_1, src_map_2], [keys_1, keys_2]):
      for map_id, a_key in a_key_list:
        if map_id == 1:
          a_mapping[a_key] = src_1_copy[a_key]
        elif map_id == 2:
          a_mapping[a_key] = src_2_copy[a_key]

  @staticmethod
  def adapt_seq_cx_one_point(ind1, ind2):
    if not isinstance(ind1, collections.abc.MutableMapping):
      raise TypeError(
        'First individual passed to OnePointMappingCrossover is not a ' +
        'MutableMapping'
      )
    if not isinstance(ind2, collections.abc.MutableMapping):
      raise TypeError(
        'Second individual passed to OnePointMappingCrossover is not a ' +
        'MutableMapping'
      )
    child1 = OnePointMappingCrossover.mapping_keys_to_tuples(1, ind1)
    child2 = OnePointMappingCrossover.mapping_keys_to_tuples(2, ind2)
    tools.cxOnePoint(child1, child2)
    OnePointMappingCrossover.blend_mappings_using_tuples(
      ind1,
      ind2,
      child1,
      child2
    )
    return (ind1, ind2)

  def __init__(self, **kwargs):
    super(OnePointMappingCrossover, self).__init__()

  def configure_toolbox(self, toolbox):
    toolbox.register('mate', OnePointMappingCrossover.adapt_seq_cx_one_point)

class FlipBitMutation(ToolboxContributor):
  def __init__(self, **kwargs):
    super(FlipBitMutation, self).__init__()
    self.indv_bit_mut_prob = float(kwargs.get('indv_bit_mut_prob', '0.05'))
  
  def configure_toolbox(self, toolbox):
    toolbox.register('mutate', tools.mutFlipBit, indpb=self.indv_bit_mut_prob)

# vim: set ts=2 sw=2 expandtab:
