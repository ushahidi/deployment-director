from DeploymentDirector.rules import ActionSettings, ParamValueAssignation

from voluptuous import Schema
import yaml
import pytest

action_settings = ActionSettings.binding()

settings_1 = """
enabled: True
labels:
  label1: value1
parameters:
  param1: one value
  param2: [two, values]
"""
settings_1 = yaml.load(settings_1)

settings_2 = """
parameters:
  the_repo: ${repo}
  the_branch: ${branch}
  the_ref: "${repo}#${branch}"
"""
settings_2 = yaml.load(settings_2)


@pytest.mark.parametrize('settings', [ settings_1, settings_2 ])
def test_action_settings(settings, context):
  def unwind(obj):
    if type(obj) in (list,tuple,set):
      for v in obj: unwind(v)
    elif type(obj) == dict:
      for v in obj.values(): unwind(v)
    else:
      yield v
  x = action_settings(settings)
  assert(isinstance(x, ActionSettings))
  assert(all([isinstance(p,ParamValueAssignation) for p in x.parameters.values()]))
  print x.parameters
  x = x.resolve(context)
  print x.parameters
  assert(isinstance(x, ActionSettings))
  assert(all([type(p) in (str,bool,int) for (k,p) in unwind(x.parameters.items())]))
