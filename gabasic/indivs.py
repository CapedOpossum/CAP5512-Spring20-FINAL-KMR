# pylint: disable=no-member

import array
import random
from deap import creator
from deap import base
from deap import tools


class BitString(object):
  def __init__(self, fitness_type, **kwargs):
    super(BitString, self).__init__()
    fitness=creator.__dict__[fitness_type]
    creator.create(
      'BitString',
      array.array,
      typecode='b',
      fitness=fitness
    )
    self._private_toolbox = base.Toolbox()
    self._bit_string = creator.__dict__['BitString']
    self.bitstring_size = int(kwargs.get('bitstring_size', 10))

  def configure_toolbox(self, toolbox):
    self._private_toolbox.register('bitstring_bool_gen', random.randint, 0, 1)
    toolbox.register(
      'individual',
      tools.initRepeat,
      self._bit_string,
      self._private_toolbox.bitstring_bool_gen,
      self.bitstring_size
    )
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

# vim: set ts=2 sw=2 expandtab:
