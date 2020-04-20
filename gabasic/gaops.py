import collections
from functools import partial
from deap import tools
from . import ToolboxContributor

class OnePointCrossover(ToolboxContributor):
  def __init__(self, **kwargs):
    super(OnePointCrossover, self).__init__()
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'mate',
      tools.cxOnePoint
    )

class TwoPointCrossover(ToolboxContributor):
  def __init__(self, **kwargs):
    super(TwoPointCrossover, self).__init__()
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'mate',
      tools.cxTwoPoint
    )

class UniformCrossover(ToolboxContributor):
  def __init__(self, **kwargs):
    super(UniformCrossover, self).__init__()
    self.indiv_item_cx_prob = float(kwargs.get('indiv_item_cx_prob', '0.5'))
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'mate',
      tools.cxUniform,
      indpb=self.indiv_item_cx_prob
    )

def mapping_keys_to_tuples(id, mapping):
  return [(id, a_key) for a_key in mapping.keys()]

def mapping_deep_copy(src_mapping):
  result = {}
  result.update(src_mapping)
  return result

def blend_mappings_using_tuples(src_map_1, src_map_2, keys_1, keys_2):
  src_1_copy = mapping_deep_copy(src_map_1)
  src_2_copy = mapping_deep_copy(src_map_2)
  src_map_1.clear()
  src_map_2.clear()
  for a_mapping, a_key_list in zip([src_map_1, src_map_2], [keys_1, keys_2]):
    for map_id, a_key in a_key_list:
      if map_id == 1:
        a_mapping[a_key] = src_1_copy[a_key]
      elif map_id == 2:
        a_mapping[a_key] = src_2_copy[a_key]

class MappingCrossoverBase(ToolboxContributor):
  @staticmethod
  def raise_no_mapped(ind1, ind2):
    raise TypeError(
      'Second individual passed to MappingCrossoverBase is not a ' +
      'MutableMapping'
    )

  def __init__(self, **kwargs):
    super(MappingCrossoverBase, self).__init__()
    self.mapped_deap_cx = MappingCrossoverBase.raise_no_mapped
  
  def __call__(self, ind1, ind2):
    if not isinstance(ind1, collections.abc.MutableMapping):
      raise TypeError(
        'First individual passed to MappingCrossoverBase is not a ' +
        'MutableMapping'
      )
    if not isinstance(ind2, collections.abc.MutableMapping):
      raise TypeError(
        'Second individual passed to MappingCrossoverBase is not a ' +
        'MutableMapping'
      )
    child1 = mapping_keys_to_tuples(1, ind1)
    child2 = mapping_keys_to_tuples(2, ind2)
    if self.mapped_deap_cx is None:
      raise RuntimeError(
        'MappingCrossoverBase not iniailized with DEAP ' +
        'operator to adapt.'
      )
    self.mapped_deap_cx(child1, child2)
    blend_mappings_using_tuples(
      ind1,
      ind2,
      child1,
      child2
    )
    return (ind1, ind2)
  
  def configure_toolbox(self, toolbox):
    toolbox.register('mate', self)
    

class OnePointMappingCrossover(MappingCrossoverBase):
  def __init__(self, **kwargs):
    super(OnePointMappingCrossover, self).__init__()
    self.mapped_deap_cx = tools.cxOnePoint

class TwoPointMappingCrossover(MappingCrossoverBase):
  def __init__(self, **kwargs):
    super(TwoPointMappingCrossover, self).__init__()
    self.mapped_deap_cx = tools.cxTwoPoint

class UniformMappingCrossover(MappingCrossoverBase):
  def __init__(self, **kwargs):
    super(UniformMappingCrossover, self).__init__()
    self.indiv_item_cx_prob = float(kwargs.get('indiv_item_cx_prob', '0.5'))
    self.mapped_deap_cx = partial(
      tools.cxUniform,
      indpb=self.indiv_item_cx_prob
    )

class FlipBitMutation(ToolboxContributor):
  def __init__(self, **kwargs):
    super(FlipBitMutation, self).__init__()
    self.indv_bit_mut_prob = float(kwargs.get('indv_bit_mut_prob', '0.05'))
  
  def configure_toolbox(self, toolbox):
    toolbox.register('mutate', tools.mutFlipBit, indpb=self.indv_bit_mut_prob)

class GaussianMutation(ToolboxContributor):
  def __init__(self, **kwargs):
    super(GaussianMutation, self).__init__()
    self.mean = float(kwargs.get('mean', '0.0'))
    self.stddev = float(kwargs.get('stddev', '0.2'))
    self.indiv_item_mut_prob = float(kwargs.get('indiv_item_mut_prob', '0.05'))
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'mutate',
      tools.mutGaussian,
      mu=self.mean,
      sigma=self.stddev,
      indpb=self.indiv_item_mut_prob
    )

# vim: set ts=2 sw=2 expandtab:
