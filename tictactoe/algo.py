from gabasic import SimpleGa


class TicTacToeGa(SimpleGa):
  def __init__(self, toolbox_mods, **kwargs):
    super(TicTacToeGa, self).__init__(toolbox_mods, **kwargs)
  
  def run(self):
    # ------------------------------
    # TODO: Add pre-GA run code here
    # ------------------------------
    population, logbook = super().run()
    # -------------------------------
    # TODO: Add post-GA run code here
    # Hall of fame available through instance field `self.hof`
    # -------------------------------

# vim: set ts=2 sw=2 expandtab:
