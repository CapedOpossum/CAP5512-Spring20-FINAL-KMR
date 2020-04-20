from deap import tools, base
from . import ToolboxContributor


class TournamentSelection(ToolboxContributor):
  def __init__(self, **kwargs):
    super(TournamentSelection, self).__init__()
    self.tournament_size = int(kwargs.get('tournament_size', '2'))
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'select',
      tools.selTournament,
      tournsize=self.tournament_size
    )

class ProportionalSelection(ToolboxContributor):
  def __init__(self, **kwargs):
    super(ProportionalSelection, self).__init__()
    self.fit_attr = kwargs.get('fit_attr', 'fitness')
  
  def configure_toolbox(self, toolbox):
    toolbox.register(
      'select',
      tools.selRoulette,
      fit_attr=self.fit_attr
    )

# vim: set ts=2 sw=2 expandtab:
