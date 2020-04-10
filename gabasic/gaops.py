from deap import tools


class TwoPointCrossover(object):
  def __init__(self, **kwargs):
    super(TwoPointCrossover, self).__init__()
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'mate',
      tools.cxTwoPoint
    )

class FlipBitMutation(object):
  def __init__(self, **kwargs):
    super(FlipBitMutation, self).__init__()
    self.indv_bit_mut_prob = float(kwargs.get('indv_bit_mut_prob', '0.05'))
  
  def configure_toolbox(self, toolbox):
    toolbox.register('mutate', tools.mutFlipBit, indpb=self.indv_bit_mut_prob)

# vim: set ts=2 sw=2 expandtab:
