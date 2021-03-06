#!/usr/bin/env python

from __future__ import absolute_import
import os
from collections import OrderedDict
from frozendict import frozendict

from .rules import *
from .utils import eprint, envdict

# The deployment director compiles a context, consisting of:
# ci:
#  ... information coming from the ci ...
# env:
#  ... environment variables ...
# repo: ... shortcut to ci['repo_name']
# branch: .. shortcut to ci['branch']
class Context(object):

  __slots__ = [ '_ci', '_env' ]

  def __init__(self, options, env={}):
    self._env = envdict(os.environ) if len(env) == 0 else envdict(env)
    if options.get('ci_name') == 'codeship':
      self._load_civars_codeship()
    else:
      self._ci = frozendict({})

  def getstr(self, key):
    return ("{self.%s}" % key).format(self=self)

  def _load_civars_codeship(self):
    self._ci = frozendict(
      branch= self.env.get('CI_BRANCH'),
      build_id= self.env.get('CI_BUILD_ID'),
      committer_email= self.env.get('CI_COMMITTER_EMAIL'),
      committer_name= self.env.get('CI_COMMITTER_NAME'),
      committer_username= self.env.get('CI_COMMITTER_USERNAME'),
      commit_description= self.env.get('CI_COMMIT_DESCRIPTION'),
      commit_id= self.env.get('CI_COMMIT_ID'),
      commit_message= self.env.get('CI_COMMIT_MESSAGE'),
      name= self.env.get('CI_NAME'),
      project_id= self.env.get('CI_PROJECT_ID'),
      repo_name= self.env.get('CI_REPO_NAME'),
      string_time= self.env.get('CI_STRING_TIME'),
      timestamp= self.env.get('CI_TIMESTAMP')
    )

  @property
  def ci(self):
    return self._ci

  @property
  def env(self):
    return self._env

  # shortcuts
  @property
  def repo(self):
    return self.ci.get('repo_name')

  @property
  def branch(self):
    return self.ci.get('branch')

  def __repr__(self):
    return 'Context(ci=%s,env=%s)' % (repr(self.ci), repr(self.env))


class DeploymentDirector(object):

  def _elog(self, v_level, *args):
    if self.options.get('verbose', 0) >= v_level:
      for arg in args:
        eprint(arg)

  """
  """
  def __init__(self, rules, options={}, env={}, env_overwrite={}):
    from copy import copy
    self.options = options
    self.actions = OrderedDict()
    self.context = Context(options, env)
    #
    self._elog(1, '* Using context: %s' % repr(self.context))
    #
    self.parse_rules(rules)

  def parse_rules(self, rules):
    # Verify schema
    rules = RulesFile.parse(rules)

    # Go through each of the rules
    for rule in rules.rules:
      self._elog(1,
        '* evaluating rule: ',
        '  ' + repr(rule))
      rule.eval(context=self.context, actions=self.actions)

    # Print the actions
    self._elog(1, '* resulting actions: ')
    for action in self.actions:
      self._elog(1,
        '  - ' + repr(action),
        '    = ' + repr(self.actions[action]))

  def run_deployment(self):
    all_actions_ok = True
    # If not dry run, execute actions
    if not self.options.get('dry_run'):
      for (name,action) in self.actions.items():
        eprint('\n\n')
        eprint('----++++ ACTION: %s ++++----' % name)
        eprint('\n\n')
        success = action.execute()
        if success == True:
          eprint("\n++++---- action OK ----++++\n")
        elif success == False:
          eprint("\n++++---- action FAILED ----++++\n")
          all_actions_ok = False
        elif success is None:
          eprint("\n++++---- action SKIPPED ----++++\n")
        else:
          eprint("\n++++---- action RESULT UNKNOWN ----++++\n")
          all_actions_ok = False

    return all_actions_ok
