#!/usr/bin/env python

class TreeConverter:
  """ The base tree converter class."""
  def __init__(self, filename=None):
    self.filename = filename
    return

  def ThrowNotImplementedError(self, tree):
    raise NotImplementedError("Convert%s not implemented."%(tree.__class__.__name__.capitalize()))

  def ConvertTree(self, tree):
    method = "Convert" + tree.__class__.__name__.capitalize()
    visitor = getattr(self, method, self.ThrowNotImplementedError)
    return visitor(tree)
