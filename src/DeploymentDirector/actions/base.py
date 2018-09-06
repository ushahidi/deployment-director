#!/usr/bin/env python

from abc import abstractmethod

class BaseAction(object):
  def __init__(self, **kwargs):
    self.enabled = True
    self.params = {}
    self.labels = {}
    self.executed = False
    self.succeeded = None

  def update_settings(self, settings):
    if hasattr(settings, 'enabled'):
      self.enabled = settings.enabled
    if hasattr(settings, 'parameters'):
      self.update_parameters(settings.parameters)
    if hasattr(settings, 'labels'):
      self.update_parameters(settings.labels)

  def update_parameters(self, params):
    self.params.update(params)

  def update_labels(self, labels):
    self.labels.update(labels)

  def execute(self):
    if self.enabled:
      ret = self.execute_action()
      self.executed = True
      self.succeeded = ret
      return ret

  @abstractmethod
  def execute_action(self):
    """
    An action must do something!
    """
    pass
