from DeploymentDirector.rules import MatchSpec

import voluptuous
import pytest

match_spec = MatchSpec.binding()

_match_spec_schema_ok = [
  'master',
  'development',
  '/release-\d+/',
  { 'match': 'master' },
  { 'match': 'master', 'as': 'MASTER' },
  { 'match': '/release-\d+', 'as': 'RELEASE' }
]

_match_spec_schema_fail = [
  1,
  True,
  1.01,
  { 'x': 1, 'y': 2},
  [ 'str1', 'str2' ],
  { 'as': 'something' }
]

@pytest.mark.parametrize('x', _match_spec_schema_ok)
def test_match_spec_schema_ok(x):
  # successful parsing
  assert isinstance(match_spec(x), MatchSpec)
  assert hasattr(match_spec(x), 'match')

@pytest.mark.parametrize('x', _match_spec_schema_fail)
def test_match_spec_schema_fail(x):
  # erroneous parsing
  with pytest.raises(voluptuous.error.Error):
    match_spec(x)


_match_spec_re_ok = [
  ('/release-.*/', 'release-20170808'),
  ('/v(\d\.?)+/', 'v0.0.1'),
]

_match_spec_re_fail = [
  ('/release-.*/', 'RELEASE-20170808'),   # case sensitive
  ('/v(\d\.?)+/', 'v0.0.1a'),             # whole string match
]

@pytest.mark.parametrize('x,value', _match_spec_re_ok)
def test_match_re_ok(x, value):
  m = match_spec(x)
  assert isinstance(m, MatchSpec)
  assert m.match_re
  assert m.test_match(value)

@pytest.mark.parametrize('x,value', _match_spec_re_fail)
def test_match_re_fail(x, value):
  m = match_spec(x)
  assert isinstance(m, MatchSpec)
  assert m.match_re
  assert not m.test_match(value)


_match_spec_as = [
  ({ 'match': '/release-.*/', 'as': 'RELEASE_match' }, 'release-20170808', { 'as': 'RELEASE_match' }),
  ({ 'match': '/v(\d\.?)+/', 'as': 'VERSION_match' }, 'v0.0.1', { 'as': 'VERSION_match' }),
  ({ 'match': '/v(\d\.?)+/', 'as': 'VERSION_match' }, 'v0.0.1a', False),    # re mismatch, thus False
]
@pytest.mark.parametrize('x,value,result', _match_spec_as)
def test_match_as(x, value, result):
  assert match_spec(x).test_match(value) == result
