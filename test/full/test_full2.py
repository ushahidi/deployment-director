from DeploymentDirector import DeploymentDirector

import yaml
import pytest
import os
import re

@pytest.fixture
def full2(request):
  return yaml.load(open(os.path.join(os.path.dirname(request.module.__file__), 'full2.yml')))

def test_full2(full2):
  assert(full2.has_key('version'))

  dd = DeploymentDirector(full2, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'branch1', 'CI_REPO_NAME': 'repoA' })
  assert(len(dd.actions) == 1)
  assert(dd.actions.has_key('ActionSucceed'))
  assert(dd.actions['ActionSucceed'].enabled)
  assert(dd.run_deployment())
  assert(dd.actions['ActionSucceed'].executed)

  dd = DeploymentDirector(full2, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'branch2', 'CI_REPO_NAME': 'repoA' })
  assert(len(dd.actions) == 3)
  for action_name in ['ActionSucceed', 'ActionFail', 'ActionSucceedToo']:
      assert(dd.actions.has_key(action_name))
      assert(dd.actions[action_name].enabled)
  assert(dd.run_deployment() == False)
  for action_name in ['ActionSucceed', 'ActionFail', 'ActionSucceedToo']:
      assert(dd.actions[action_name].executed)
