from __future__ import absolute_import
from .base import BaseAction
from ..utils import eprint
from collections import defaultdict

from copy import copy
import executor

class CommandAction(BaseAction):
  def __init__(self, command, env={}, **kwargs):
    super(self.__class__, self).__init__(**kwargs)
    self.command = command
    self.env = copy(env)

  @property
  def parsed_command(self):
  	return self.command.format(**self.params)

  @property
  def parsed_env(self):
  	return defaultdict(
      lambda: '',
      [(k,v.format(**self.params)) for (k,v) in self.env.items()]
    )

  def execute_action(self):
    if self.command is None:
      eprint("ERROR: No command defined for action")
      return False
    eprint("Executing command {}".format(self.parsed_command))
    return executor.execute(self.parsed_command, environment=self.parsed_env, check=False)

__all__ = [ 'CommandAction' ]
