#!/usr/bin/env python
import node
import redhawk.utils.util as U

class TreeConverter:
  """ The base tree converter class."""
  def __init__(self, filename=None):
    self.filename = filename
    return

  def ThrowNotImplementedError(self, tree):
    raise NotImplementedError("Convert%s not implemented."%(tree.__class__.__name__.capitalize()))


  def AttachParents(self, tree, parent = None):
    tree.SetParent(parent)
    for c in U.Flatten(tree.GetChildren()):
      if c is not None:
        self.AttachParents(c, tree)
    return


  def Convert(self, tree):
    """ Calls ConvertTree, and attaches parent links using __AttachParents.
    This is the method to be called by outside methods, and functions."""
    l_ast = self.ConvertTree(tree)
    self.AttachParents(l_ast)
    return l_ast


  def ConvertTree(self, tree):
    method = "Convert" + tree.__class__.__name__.capitalize()
    visitor = getattr(self, method, self.ThrowNotImplementedError)
    return visitor(tree)
