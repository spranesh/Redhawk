#!/usr/bin/env python
""" Convert C-Tree to ast. """

import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.types as T

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
    return N.Constant(GetCoords(tree), tree.value, T.BaseType(tree.type))

  def ConvertId(self, tree):
    #TODO(spranesh): Is this assert always true?
    assert(tree.name == 'NULL')
    return N.Constant(GetCoords(tree), 
        value = tree.name, 
        type = T.Pointer(T.BaseType('NULL')))

  def ConvertDecl(self, tree):
    # TODO(spranesh): Handle quals, storage, etc..
    t = self.ConvertTree(tree.type)
    if isinstance(t, N.DeclareFunction):
      t.name = tree.name
      return t
    else: 
      return N.DefineVariable(GetCoords(tree), 
        name = tree.name, 
        init = self.ConvertTree(tree.init),
        type = t)

  def ConvertTypename(self, tree):
    #TODO(spranesh): Handle quals.
    t = self.ConvertTree(tree.type)
    return N.DefineVariable(None, # No coords for Typename
        name = tree.name,
        type = t)

  def ConvertTypedecl(self, tree):
    """ Returns Type Object """
    return T.BaseType(tree.type.names[0])

  def ConvertPtrdecl(self, tree):
    # TODO(spranesh): Handle quals (such as constants)
    """ Returns Type Object """
    return T.Pointer(self.ConvertTree(tree.type))

  def ConvertArraydecl(self, tree):
    # TODO(spranesh): Handle array dimensions.
    """ Returns Type Object """
    return T.Array(self.ConvertTree(tree.type))

  def ConvertNonetype(self, tree):
    """ To handle cases when children might be none."""
    return None

  def ConvertFuncdecl(self, tree):
    return N.DeclareFunction(
        position = GetCoords(tree),
        name = None,
        arguments = map(self.ConvertTree, tree.args.params),
        return_type = self.ConvertTree(tree.type))


