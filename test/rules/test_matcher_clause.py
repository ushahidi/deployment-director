from __future__ import absolute_import
from DeploymentDirector.rules import MatcherClause
from DeploymentDirector.director import Context

import voluptuous
import pytest

matcher_clause = MatcherClause.binding()

_matcher_clause_schema_ok = [
  {'repo': 'my-repo', 'branch': 'my-branch'},
  {'repo': 'my-repo', 'branch': [ 'my-branch' ]},
  {'branch': [ 'branch1', 'branch2' ]}
]

_matcher_clause_schema_fail = [
  {'x': 1},
  'string', 1, True,
  [{'repo': 'my-repo'}],
  {'stuff': 'should-match'},
  {'branch': { 'x': 1 }},
  {'repo': True},
  {'repo': 1}
]

@pytest.mark.parametrize('x', _matcher_clause_schema_ok)
def test_matcher_clause_schema_ok(x):
  # successful parsing
  assert isinstance(matcher_clause(x), MatcherClause)

@pytest.mark.parametrize('x', _matcher_clause_schema_fail)
def test_matcher_clause_schema_fail(x):
  # erroneous parsing
  with pytest.raises(voluptuous.error.Error):
    matcher_clause(x)

def test_matcher_match(context):
  # positive match tests
  assert(matcher_clause({ 'repo': context.repo }).test(context))
  assert(matcher_clause({ 'branch': context.branch }).test(context))
  assert(matcher_clause({ 'repo': context.repo, 'branch': context.branch }).test(context))
  assert(matcher_clause({ 'repo': [ 'other', 'repos', context.repo ]}).test(context))
  assert(matcher_clause({ 'branch': [ 'other', 'branches', context.branch ]}).test(context))
  assert(matcher_clause({
    'repo': [ 'other', 'repos', context.repo ],
    'branch': [ 'other', 'branches', context.branch ]
    }).test(context))
  # negative match tests
  assert(not matcher_clause({ 'repo': 'xyz' }).test(context))
  assert(not matcher_clause({ 'branch': 'xyz' }).test(context))
  assert(not matcher_clause({ 'repo': context.repo, 'branch': 'xyz' }).test(context))
  assert(not matcher_clause({ 'repo': [ 'other', context.repo ], 'branch': 'xyz' }).test(context))
  assert(not matcher_clause({ 'repo': 'xyz', 'branch': context.branch }).test(context))
