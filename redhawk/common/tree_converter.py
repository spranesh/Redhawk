#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from . import node as N
from . import node_position as NP
import redhawk.utils.util as U

class TreeConverter:
  """ The base tree converter class."""
  def __init__(self, filename=None):
    self.filename = filename
    return

  def ThrowNotImplementedError(self, tree):
    raise NotImplementedError("Convert%s not implemented."%(tree.__class__.__name__.capitalize()))


  def AttachParents(self, tree, parent = None):
    """ Attach parents to the tree.
    Also create the cache at the each node, by exercising
    tree.GetFlattenedChildren()."""
    tree.SetParent(parent)
    for c in tree.GetFlattenedChildren():
      if c is not None:
        try:
          self.AttachParents(c, tree)
        except AttributeError as e:
          print(c, parent, tree)
          raise AttributeError(e)
    return


  def Convert(self, tree):
    """ Calls ConvertTree, and attaches parent links using AttachParents.
    This is the method to be called by outside methods, and functions.

    This also exercises the GetFlattenedChildren at each node, and creates the
    necessary cache at each node. If this is not done during the database
    creation time, it is rather pointless, since every node is most likely to be
    visited just once during the course of a search."""

    if tree is None:
      l_ast = N.Module(position = NP.NodePosition(self.filename, 1, 1),
        filename = self.filename,
        children = [])

    else:
      l_ast = self.ConvertTree(tree)

    self.AttachParents(l_ast)
    return l_ast

  def ConvertTree(self, tree):
    method = "Convert" + tree.__class__.__name__.capitalize()
    visitor = getattr(self, method, self.ThrowNotImplementedError)
    return visitor(tree)

  def ConvertListOfStatements(self, statements):
    """ Convert a list of statements, to a list of LAST nodes.
    Note that this function returns a List and not a Node."""
    return list(map(self.ConvertTree, statements))
