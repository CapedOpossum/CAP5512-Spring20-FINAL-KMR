
class ToolboxContributor(object):
  def __init__(self):
    super(ToolboxContributor, self).__init__()
  
  def configure_toolbox(self, toolbox):
    raise NotImplementedError(
      'ToolboxContributor missing configure_toolbox() implementation.'
    )

# vim: set ts=2 sw=2 expandtab:
