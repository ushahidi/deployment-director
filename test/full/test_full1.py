from DeploymentDirector import DeploymentDirector

import yaml
import pytest
import os
import re

@pytest.fixture
def full1(request):
  return yaml.load(open(os.path.join(os.path.dirname(request.module.__file__), 'full1.yml')))

def test_full1(full1):
  assert(full1.has_key('version'))

  dd = DeploymentDirector(full1, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'master', 'CI_REPO_NAME': 'platform' })
  assert(len(dd.actions) == 1)
  assert(dd.actions.has_key('deploy'))
  assert(not dd.actions['deploy'].enabled)

  with pytest.raises(KeyError): # missing BUILD_LOCATION environment variable
    dd = DeploymentDirector(full1, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'production', 'CI_REPO_NAME': 'platform' })

  dd = DeploymentDirector(full1, { 'ci_name': 'codeship' }, { 'CI_BRANCH': 'production', 'CI_REPO_NAME': 'platform' , 'BUILD_LOCATION': '/var/tmp' })
  assert(len(dd.actions) == 1)
  assert(dd.actions.has_key('deploy'))
  assert(dd.actions['deploy'].enabled)
  assert(re.sub("\s+", " ", dd.actions['deploy'].parsed_command).strip() ==
    "ush-ansible-playbook.sh -vv -i hosts/rackspace_prod.yml platform-api-update.yml -e PLATFORM_CLIENT_DEPLOY_SRC=\"/var/tmp\"")
  assert(dd.actions['deploy'].parsed_env['ANSIBLE_GITHUB_REPO'] == 'platform-ansible-cloud')
