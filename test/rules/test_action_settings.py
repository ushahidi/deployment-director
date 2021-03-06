from __future__ import absolute_import
from __future__ import print_function
from DeploymentDirector.rules import ActionSettings, ParamValueAssignation, Match

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
settings_1 = yaml.safe_load(settings_1)

settings_2 = """
parameters:
  the_repo: ${repo}
  the_branch: ${branch}
  the_ref: "${repo}#${branch}"
"""
settings_2 = yaml.safe_load(settings_2)


@pytest.mark.parametrize('settings', [ settings_1, settings_2 ])
def test_action_settings(settings, match):
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
  print(x.parameters)
  x = x.resolve(match)
  print(x.parameters)
  assert(isinstance(x, ActionSettings))
  assert(all([type(p) in (str,bool,int) for (k,p) in unwind(list(x.parameters.items()))]))
