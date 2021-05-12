from __future__ import absolute_import
from DeploymentDirector.rules import ParamValueAssignation

import pytest

param_value_assignation = ParamValueAssignation.binding()

@pytest.mark.parametrize('x', [ 1, 'abc', True ])
def test_scalar_params(x, match):
  pv = param_value_assignation(x)
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == x)

def test_interpolate_params(match):
  pv = param_value_assignation('${repo}')
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == match.context.repo)
  
  pv = param_value_assignation('${branch}')
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == match.context.branch)
  
  pv = param_value_assignation(['${repo}', '${branch}'])
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == [ match.context.repo, match.context.branch ])

  pv = param_value_assignation({ 'value': { 'the_repo': '${repo}' } })
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == { 'the_repo': match.context.repo })

def test_map_params(match):
  pv = param_value_assignation({
    'key': 'repo',
    'map': {
      match.context.repo: 'x${repo}x',
      'other': 'other'
      }
    })
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == 'x%sx' % match.context.repo)

def test_map_params_with_match_as(match_branch_as_DEFAULT):
  match = match_branch_as_DEFAULT
  pv = param_value_assignation({
    'key': 'branch',
    'map': {
      'DEFAULT': 'x${branch}x',
      'other': 'other'
      }
    })
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == 'x%sx' % match.context.branch)

def test_map_params_match_priorities(match_branch_as_DEFAULT):
  match = match_branch_as_DEFAULT
  pv = param_value_assignation({
    'key': 'branch',
    'map': {
      match.context.branch: 'x${branch}x',    # this will match first
      'DEFAULT': 'y${branch}y',
      'other': 'other'
      }
    })
  assert(isinstance(pv, ParamValueAssignation))
  assert(pv.resolve(match) == 'x%sx' % match.context.branch)
