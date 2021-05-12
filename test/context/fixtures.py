from __future__ import absolute_import
import pytest

from DeploymentDirector.director import Context
from DeploymentDirector.rules import Match


# def pytest_generate_tests(metafunc):
#   if 'context' in metafunc.fixturenames:
#     metafunc.parametrize("context", envs.keys(), indirect=True)

envs={
  'complete': {
    'CI_BRANCH': 'master',
    'CI_BUILD_ID': '1313-313131-3183818-3131',
    'CI_COMMITTER_EMAIL': 'boss@company.com',
    'CI_COMMITTER_NAME': 'Your Boss',
    'CI_COMMITTER_USERNAME': 'da_b0ss',
    'CI_COMMIT_DESCRIPTION': 'Revise Salaries',
    'CI_COMMIT_ID': 'd6cd1e2bd19e03a81132a23b2025920577f84e37',
    'CI_COMMIT_MESSAGE': 'just yours',
    'CI_NAME': 'codeship',
    'CI_PROJECT_ID': 'abcdef-aabbcc-ffffff-ababab',
    'CI_REPO_NAME': 'company-salaries',
    'CI_STRING_TIME': '2017-10-13T10:14:23+00:00',
    'CI_TIMESTAMP': '1507889663',
    'EXTRA_KEY': 'extra_value',
    }
  }

@pytest.fixture(params=list(envs.keys()), ids=list(envs.keys()))
def context(request):
  return Context(options={'ci_name': 'codeship'}, env=envs[request.param] )

@pytest.fixture
def match(context):
  return Match(matcher_clause=None, context=context)

@pytest.fixture
def match_branch_as_DEFAULT(context):
  return Match(matcher_clause=None, context=context, matched_as={ 'branch': 'DEFAULT' })
