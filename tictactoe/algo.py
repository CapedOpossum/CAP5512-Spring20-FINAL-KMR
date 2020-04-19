from deap import tools
from gabasic import SimpleGa
from .indiv import  PolicyGene
import jsonpickle
import json
import numpy as np


class TicTacToeGa(SimpleGa):
  def __init__(self, toolbox_mods, **kwargs):
    super(TicTacToeGa, self).__init__(toolbox_mods, **kwargs)
    # Replace single fitness statistics with multi-statistics to log individual
    # size.
    stats_len = tools.Statistics(key=len)
    stats_len.register('avg', np.mean)
    stats_len.register('max', np.max)
    multi_stats = tools.MultiStatistics(fitness=self.stats, length=stats_len)
    self.stats = multi_stats
  
  def run(self):
    # ------------------------------
    # TODO: Add pre-GA run code here
    # ------------------------------
    population, logbook = super().run()
    # -------------------------------
    # TODO: Add post-GA run code here
    # Hall of fame available through instance field `self.hof`
    # -------------------------------

    PolicyGeneStateDomain = jsonpickle.encode(PolicyGene.state_domain, unpicklable=False)
    BestIndividual = jsonpickle.encode(self.hof, unpicklable=False)

    file = open("PolicyGeneStateDomain.json", "w")
    file.write(PolicyGeneStateDomain)
    file.close()

    file = open("BestIndividual.json", "w")
    file.write(BestIndividual)
    file.close

    return population, logbook

# vim: set ts=2 sw=2 expandtab:
