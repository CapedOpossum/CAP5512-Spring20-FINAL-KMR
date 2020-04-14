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

# vim: set ts=2 sw=2 expandtab:
