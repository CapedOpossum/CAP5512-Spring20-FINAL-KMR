
class SumItems(object):
  def __init__(self, **kwargs):
    super(SumItems, self).__init__()

  def configure_toolbox(self, toolbox):
    toolbox.register('evaluate', self)

  def __call__(self, individual):
    return (sum(individual),)

# vim: set ts=2 sw=2 expandtab:
