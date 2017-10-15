from DeploymentDirector.rules import ParamValueAssignation

import pytest

param_value_assignation = ParamValueAssignation.binding()

@pytest.mark.parametrize('x', [ 1, 'abc', True ])
def test_scalar_params(x, context):
  pv = param_value_assignation(x)
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(context) == x)

def test_interpolate_params(context):
  pv = param_value_assignation('${repo}')
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(context) == context.repo)
  
  pv = param_value_assignation('${branch}')
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(context) == context.branch)
  
  pv = param_value_assignation(['${repo}', '${branch}'])
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(context) == [ context.repo, context.branch ])

  pv = param_value_assignation({ 'value': { 'the_repo': '${repo}' } })
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(context) == { 'the_repo': context.repo })

def test_map_params(context):
  pv = param_value_assignation({
    'key': 'repo',
    'map': {
      context.repo: 'x${repo}x',
      'other': 'other'
      }
    })
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(context) == 'x%sx' % context.repo)
