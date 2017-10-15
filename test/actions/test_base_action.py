from DeploymentDirector.actions.base import BaseAction
from DeploymentDirector.rules import ActionSettings

class DummyAction(BaseAction):
  def execute_action(self):
    return True

def test_base_action():
  a = DummyAction()
  assert(a.enabled)
  assert(a.execute() is True)
  assert(a.params == {})
  assert(a.labels == {})

  a.update_settings(ActionSettings(enabled=False))
  assert(not a.enabled)
  assert(a.execute() is None)

  a.update_settings(ActionSettings(parameters={ 'param1': 'value1' }))
  assert(a.params.has_key('param1'))

  a.update_settings(ActionSettings(parameters={ 'param2': 'value2' }))
  assert(a.params.has_key('param1') and a.params.has_key('param2'))

