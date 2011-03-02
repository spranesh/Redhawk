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

  # We first handle all declarations
  # Decl is simply a declaration of a function, variable, array, or pointer
  #   FuncDecl - Function declaration
  #   PtrDecl - Pointer declaration
  #   ArrayDecl - Array declaration
  # TypeDecl  - a base type declaration

  def ConvertTypedecl(self, tree):
    """ Converts Type Declarations. These are base type declarations, and
    have declname, quals, and an IdentifierType child (which we deal
    with in this function itself)."""
    n = N.Node('type', position=ConvertCoordinates(tree.coord))
    n.AddProperty('name', tree.declname)
    n.AddProperty('quals', tree.quals)
    n.AddProperty('type', tree.type.names[0])
    # TODO(spranesh): Does the above (IdentifierType.names) have only element
    # always?
    return n

  def ConvertPtrdecl(self, tree):
    """ Converts Pointer Declarations. Pointer declarations only contain
    qualifiers, and a type child."""
    n = N.Node('pointer-to', position=ConvertCoordinates(tree.coord))
    n.AddProperty('quals', tree.quals)
    n.AddChild(self.ConvertTree(tree.type))
    return n

  def ConvertArraydecl(self, tree):
    """ Converts Array Declarations. Array Declarations contain two children -
    a type child, and a dimension (constant)."""
    n = N.Node('array-of', position=ConvertCoordinates(tree.coord))
    n.AddChild(self.ConvertTree(tree.type))
    n.AddChild(self.ConvertTree(tree.dimension))
    return n

  def ConvertFuncdecl(self, tree):
    """ Convert Function Declarations. Function declarations contain two
    children - type and args, meant to simulate: 

    type <name>(args);

    The name of the function, `name`, can be obtained from the type
    declaration. TODO(spranesh): ALWAYS the case? What about function
    typedefs?
    """
    n = N.Node('declare-function', position=ConvertCoordinates(tree.coord))

    if tree.args is not None:
      for arg in tree.args.children():
        n.AddChild(self.ConvertTree(arg))

    type_property = self.ConvertTree(tree.type)
    # Do not store the type here. Instead store return type as type.
    n.AddProperty('type', type_property)
    n.AddProperty('name', type_property.GetProperty('name'))
    return n

  def ConvertDecl(self, tree):
    """ Converts a Declaration. A declaration consists of:
        name, quals, storage, funcspec
    and children:
        type, init, bitsize"""

    n = N.Node('define-variable', position=ConvertCoordinates(tree.coord))
    # TODO(spranesh): Should these be properties? Or Children?
    if tree.init is not None:
      n.AddProperty('init', self.ConvertTree(tree.init))
    if tree.bitsize is not None:
      n.AddProperty('bitsize', self.ConvertTree(self.bitsize))

    n.AddPropertiesFrom(tree, 
        ["name", "quals", "storage", "funcspec"])

    t = self.ConvertTree(tree.type)
    n.AddProperty('type', t.type)
    return n

  def ConvertFuncdef(self, tree):
    """ Convert Function Definitions. Function Definitions consist of
    a two children - a declaration and a body. It also has an optional
    K&R style parameter declarations, a list of children. This is currently
    not supported. TODO(spranesh): Decided support for old K&R type
    arguments?
    
    The resulting function definition node has the form

    (define-function name '(properties)
      (args)
      (body))

    A typical function definition parse tree part looks like:
    FuncDef:
      Decl:
        FuncDecl:
          ParamList:
          ...
          TypeDecl: main, []
            IdentifierType: ['int']
      Compound:
        Return:
          Constant: int, 0

    We steal the name from the declaration, and mould the function declare
    agnostic ast, so as to make the representation more succint.
    """
    n = N.Node('define-function', position=ConvertCoordinates(tree.coord))
    decl = tree.decl
    ast_func_decl = self.ConvertTree(decl.type)
    n.AddProperty('type', ast_func_decl.GetProperty('type'))
    # TODO(spranesh): Rename function-type to type?
    # n.AddProperty('function-type', ast_func_decl)

    # Some of these must be made tags?
    n.AddPropertiesFrom(decl, 
        ["name", "bitsize", "quals", "init", "storage", "funcspec"])

    # TODO(spranesh): Avoid this recomputation (of converting arguments).
    args = decl.type.args
    if args is not None:
      a = N.Node('arguments', position=ConvertCoordinates(args.coord))
      for arg in args.children():
        a.AddChild(self.ConvertTree(arg))
    else:
      a = N.Node('arguments', position=None)
    n.AddChild(a)

    n.AddChild(self.ConvertTree(tree.body))
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

  def ConvertBinaryop(self, tree):
    n = N.Node('binary-op', position=ConvertCoordinates(tree.coord))
    n.AddProperty('op', tree.op)
    n.AddChild(self.ConvertTree(tree.left))
    n.AddChild(self.ConvertTree(tree.right))
    return n
