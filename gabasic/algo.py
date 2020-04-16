# pylint: disable=no-member

import numpy as np
from deap import algorithms, tools, base


class SimpleGa(object):
  def __init__(self, toolbox_mods, **kwargs):
    super(SimpleGa, self).__init__()
    self.population_size = int(kwargs.get('population_size', '100'))
    self.max_generation_count = int(kwargs.get('max_generation_count', '100'))
    self.crossover_probability = float(kwargs.get('crossover_probability', '0.5'))
    self.mutation_probability = float(kwargs.get('mutation_probability', '0.1'))
    self.toolbox = base.Toolbox()
    for a_mod in toolbox_mods:
      a_mod.configure_toolbox(self.toolbox)
    self.stats = tools.Statistics(lambda ind: ind.fitness.values)
    self.stats.register('avg', np.mean)
    self.stats.register('std', np.std)
    self.stats.register('min', np.min)
    self.stats.register('max', np.max)
    self.hof = tools.HallOfFame(1)
  
  def run(self):
    population = self.toolbox.population(n=self.population_size)
    population, log = algorithms.eaSimple(
      population,
      self.toolbox,
      cxpb=self.crossover_probability,
      mutpb=self.mutation_probability,
      ngen=self.max_generation_count,
      stats=self.stats,
      halloffame=self.hof,
      verbose=True
    )
    
    return population, log

# vim: set ts=2 sw=2 expandtab:
