#!/usr/bin/env python
""" Convert C-Tree to ast. """

import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.node_types as NT

def GetCoords(t):
  assert(t is not None)
  c = t.coord
  assert(c is not None)
  return NP.NodePosition(c.file, c.line, c.column)

class CTreeConverter:
  def ThrowNotImplementedError(self, tree):
    raise NotImplementedError("Convert%s not implemented."%(tree.__class__.__name__.capitalize()))

  def ConvertTree(self, tree):
    method = "Convert" + tree.__class__.__name__.capitalize()
    visitor = getattr(self, method, self.ThrowNotImplementedError)
    return visitor(tree)

  def ConvertReturn(self, tree):
    return N.Return(GetCoords(tree), self.ConvertTree(tree.expr))

  def ConvertConstant(self, tree):
    return N.Constant(GetCoords(tree), tree.value, tree.type)
