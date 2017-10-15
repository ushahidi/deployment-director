from DeploymentDirector.actions import CommandAction
from DeploymentDirector.rules import ActionSettings

from executor import ExternalCommandFailed

import pytest

def test_command_action():
  a = CommandAction(command='test {p1} -eq {p2}')

  a.update_settings(ActionSettings(parameters={ 'p1': 1, 'p2': 1 }))
  assert(a.parsed_command == 'test 1 -eq 1')
  assert(a.execute())

  a.update_settings(ActionSettings(parameters={ 'p1': 1, 'p2': 2 }))
  assert(a.parsed_command == 'test 1 -eq 2')
  with pytest.raises(ExternalCommandFailed):
    a.execute()

def test_command_action_with_env():
  a = CommandAction(command='bash -c "test {p1} -eq $P2"', env={'P2': "1"})

  a.update_settings(ActionSettings(parameters={ 'p1': 1 }))
  assert(a.execute())

  a.update_settings(ActionSettings(parameters={ 'p1': 2 }))
  with pytest.raises(ExternalCommandFailed):
    a.execute()

def test_command_action_with_env_param():
  a = CommandAction(command='bash -c "test {p1} -eq $P2"', env={'P2': "{p2}"})

  a.update_settings(ActionSettings(parameters={ 'p1': 1, 'p2': 1 }))
  assert(a.parsed_env.has_key('P2'))
  assert(a.parsed_env['P2'] == '1')
  assert(a.execute())

  a.update_settings(ActionSettings(parameters={ 'p1': 1, 'p2': 2 }))
  assert(a.parsed_env.has_key('P2'))
  assert(a.parsed_env['P2'] == '2')
  with pytest.raises(ExternalCommandFailed):
    a.execute()
