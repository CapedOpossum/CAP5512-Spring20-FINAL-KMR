from deap import creator
from deap import base


class FitnessMax(object):
  def __init__(self, **kwargs):
    super(FitnessMax, self).__init__()
    weights_str = kwargs.get('weights', '1.0')
    weights = [float(a_weight) for a_weight in weights_str.split(',')]
    creator.create('FitnessMax', base.Fitness, weights=weights)

# vim: set ts=2 sw=2 expandtab:
