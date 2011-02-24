#!/usr/bin/env python
""" Convert C-Tree to ast. """

import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.node_types as NT

def ConvertCoordinates(c):
  return NP.NodePosition(c.file, c.line, c.column)

class CTreeConverter:
  def ThrowNotImplementedError(self, tree):
    raise NotImplementedError("Convert%s not implemented."%(tree.__class__.__name__.capitalize()))

  def ConvertTree(self, tree):
    method = "Convert" + tree.__class__.__name__.capitalize()
    visitor = getattr(self, method, self.ThrowNotImplementedError)
    return visitor(tree)

  def ConvertFileast(self, tree):
    n = N.Node('define-module')
    for i in tree.children():
      n.AddChild(self.ConvertTree(i))
    return n

  def ConvertFuncdef(self, tree):
    n = N.Node('define-function', position=ConvertCoordinates(tree.coord))
    decl = tree.decl
    return_type = self.ConvertTree(decl.type.type)
    n.AddProperty('return-type', return_type)
    # Some of these must be made tags?
    n.AddPropertiesFrom(decl, 
        ["name", "bitsize", "quals", "init", "storage", "funcspec"])

    args = decl.type.args
    a = N.Node('arguments', position=ConvertCoordinates(args.coord))
    n.AddChild(a)
    for arg in args.children():
      a.AddChild(self.ConvertTree(arg.type))

    n.AddChild(self.ConvertTree(tree.body))
    return n
    
  def ConvertTypedecl(self, tree):
    n = N.Node('define-variable', position=ConvertCoordinates(tree.coord))
    n.AddProperty('name', tree.declname)
    n.AddProperty('quals', tree.quals)
    n.AddProperty('type', tree.type.names)
    return n

  def ConvertCompound(self, tree):
    n = N.Node('begin-compound', position=ConvertCoordinates(tree.coord))
    for m in tree.block_items:
      n.AddChild(self.ConvertTree(m))
    return n

  def ConvertReturn(self, tree):
    n = N.Node('return', position=ConvertCoordinates(tree.coord))
    n.AddChild(self.ConvertTree(tree.expr))
    return n

  def ConvertConstant(self, tree):
    n = N.Node('constant', position=ConvertCoordinates(tree.coord))
    n.AddProperty('type', tree.type)
    n.AddProperty('value', tree.value)
    return n

