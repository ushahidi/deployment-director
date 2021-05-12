from __future__ import absolute_import
import pytest

def test_context(context):
  assert(context.ci not in (None,{}))
  assert(context.ci['branch'] is not None)
  assert(context.ci['repo_name'] is not None)
  assert(context.env not in (None, {}))
  assert(type(context.branch) == str)
  assert(type(context.repo) == str)
  assert(all([x for x in context.ci.values()]))

