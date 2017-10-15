from DeploymentDirector.rules import AddAction, ConfigureAction, Rule
from DeploymentDirector.actions import CommandAction

import pytest
import yaml

add_action = AddAction.binding()
configure_action = ConfigureAction.binding()
rule = Rule.binding()

a1 = """
add_action:
  name: a1
  action:
    class_name: CommandAction
    arguments:
      command: test "{param1}" == "{param2}"
  parameters:
    param1: ${repo}
    param2: ${repo}
"""
a1 = yaml.load(a1)

c1 = """
configure_action:
  action: a1
  settings:
    enabled: False
    parameters:
      param2: ${branch}
"""
c1 = yaml.load(c1)

r1 = """
when:
  
then:
  add_action:
    name: a2
    action:
      class_name: CommandAction
      arguments:
        command: true
"""

def test_actions(context):
  actions = {}
  conseq1 = add_action(a1)
  conseq1.apply(context, actions)
  assert(len(actions) > 0)
  assert(actions.has_key('a1'))
  assert(isinstance(actions['a1'], CommandAction))
  assert(actions['a1'].enabled)
  assert(actions['a1'].params.get('param1') == context.repo)
  assert(actions['a1'].params.get('param2') == context.repo)

  conseq2 = configure_action(c1)
  conseq2.apply(context, actions)
  assert(len(actions) > 0)
  assert(actions.has_key('a1'))
  assert(isinstance(actions['a1'], CommandAction))
  assert(not actions['a1'].enabled)
  assert(actions['a1'].params.get('param1') == context.repo)
  assert(actions['a1'].params.get('param2') == context.branch)

