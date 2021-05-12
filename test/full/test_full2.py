from __future__ import absolute_import
from DeploymentDirector import DeploymentDirector

import yaml
import pytest
import os
import re

@pytest.fixture
def full2(request):
  return yaml.safe_load(open(os.path.join(os.path.dirname(request.module.__file__), 'full2.yml')))

def test_full2(full2):
  assert('version' in full2)

  dd = DeploymentDirector(full2, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'branch1', 'CI_REPO_NAME': 'repoA' })
  assert(len(dd.actions) == 1)
  assert('ActionSucceed' in dd.actions)
  assert(dd.actions['ActionSucceed'].enabled)
  assert(dd.run_deployment())
  assert(dd.actions['ActionSucceed'].executed)
  assert(dd.actions['ActionSucceed'].succeeded)

  dd = DeploymentDirector(full2, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'branch2', 'CI_REPO_NAME': 'repoA' })
  assert(len(dd.actions) == 3)
  for action_name in ['ActionSucceed', 'ActionFail', 'ActionSucceedToo']:
    assert(action_name in dd.actions)
    assert(dd.actions[action_name].enabled)
  assert(dd.run_deployment() == False)
  for action_name in ['ActionSucceed', 'ActionFail', 'ActionSucceedToo']:
    assert(dd.actions[action_name].executed)
  assert(dd.actions['ActionSucceed'].succeeded)
  assert(not dd.actions['ActionFail'].succeeded)
  assert(dd.actions['ActionSucceedToo'].succeeded)

  dd = DeploymentDirector(full2, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'branch3', 'CI_REPO_NAME': 'repoA' })
  assert(len(dd.actions) == 2)
  assert(dd.run_deployment())

