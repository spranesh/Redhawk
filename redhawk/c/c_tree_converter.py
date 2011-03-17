#!/usr/bin/env python
""" Convert C-Tree to ast. """

import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.types as T

# Map C operators into the LAST operators
BINARY_OPERATOR_CONVERSIONS = {
      '+'   : 'ADD'
     ,'-'   : 'MINUS'
     ,'*'   : 'MULTIPLY'
     ,'/'   : 'DIVIDE'
     ,'^'   : 'BITWISE_XOR'
     ,'|'   : 'BITWISE_OR'
     ,'&'   : 'BITWISE_AND'
     ,'<<'  : 'LSHIFT'
     ,'>>'  : 'RSHIFT'
     ,'%'   : 'MOD'
     ,'<'   : 'LT'
     ,'>'   : 'GT'
     ,'<='  : 'LTE'
     ,'>='  : 'GTE'
     ,'=='  : 'EQ'
     ,'!='  : 'NOT_EQ'
     ,'&&'  : 'BOOLEAN_AND'
     ,'||'  : 'BOOLEAN_OR'

     ,'.'   : 'ATTRIBUTE_INDEX'
     ,'->'  : 'ARROW' # TODO(spranesh): Bad Name?
}

UNARY_OPERATOR_CONVERSIONS = {
      '+'      : 'UNARY_PLUS'
     ,'-'      : 'UNARY_MINUS'
     ,'!'      : 'BOOLEAN_NOT'
     ,'++'     : 'PRE_INCREMENT'
     ,'p++'    : 'POST_INCREMENT'
     ,'--'     : 'PRE_DECREMENT'
     ,'p--'    : 'POST_DECREMENT'
     ,'*'      : 'POINTER_DEREFERENCE'
     ,'&'      : 'ADDRESS_OF'
     ,'sizeof' : 'SIZE_OR_LEN'
     ,'~'      : 'BITWISE_NOT'
}


def GetCoords(t):
  assert(t is not None)
  c = t.coord
  assert(c is not None)
  return NP.NodePosition(c.file, c.line, c.column)

class CTreeConverter:
  def __init__(self, filename=None):
    self.filename = filename
    return

  def ThrowNotImplementedError(self, tree):
    raise NotImplementedError("Convert%s not implemented."%(tree.__class__.__name__.capitalize()))

  def ConvertTree(self, tree):
    method = "Convert" + tree.__class__.__name__.capitalize()
    visitor = getattr(self, method, self.ThrowNotImplementedError)
    return visitor(tree)

  def ConvertFileast(self, tree):
    position = NP.NodePosition(self.filename, 0, 0)
    return N.Module(self.filename,
        children = map(self.ConvertTree, tree.children()))

  def ConvertReturn(self, tree):
    return N.Return(GetCoords(tree), 
        return_expression = self.ConvertTree(tree.expr))

  def ConvertConstant(self, tree):
    return N.Constant(GetCoords(tree), 
        value = tree.value, type = T.BaseType(tree.type))

  def ConvertId(self, tree):
    #TODO(spranesh): Is this assert always true?
    if tree.name == 'NULL':
      return N.Constant(GetCoords(tree), 
          value = tree.name, 
          type = T.Pointer(T.BaseType('NULL')))
    else:
      return N.ReferVariable(GetCoords(tree), 
          name = tree.name)

  def ConvertDecl(self, tree):
    # We have to check if the child is a 
    #   a. a function declaration
    #   b. a structure declaration
    # Otherwise it is a normal declaration
    t = self.ConvertTree(tree.type)
    if isinstance(t, N.DeclareFunction):
      t.name = tree.name
      t.storage = tree.storage
      t.quals = tree.quals
      return t
    if isinstance(t, N.Structure):
      t.storage = tree.storage
      t.quals = tree.quals
      return t
    else: 
      return N.DefineVariable(GetCoords(tree), 
        name = tree.name, 
        init = self.ConvertTree(tree.init),
        type = t,
        storage = tree.storage,
        quals = tree.quals)

  def ConvertTypename(self, tree):
    #TODO(spranesh): Handle quals.
    t = self.ConvertTree(tree.type)
    return N.DefineVariable(None, # No coords for Typename
        name = tree.name,
        type = t)

  def ConvertIdentifiertype(self, tree):
    """ Returns Type Object """
    try:
      return T.BaseType(base_type = tree.names[0])
    except IndexError, e:
      # Default type is int in C
      return T.BaseType(base_type = 'int')

  def ConvertTypedecl(self, tree):
    """ Returns Type Object """
    # child is either an IdentifierType or a Struct
    t = self.ConvertTree(tree.type)
    assert(isinstance(t, T.BaseType) or isinstance(t, T.StructureType) or
        isinstance(t, N.Structure))
    return t

  def ConvertPtrdecl(self, tree):
    # TODO(spranesh): Handle quals (such as constants)
    """ Returns Type Object """
    return T.Pointer(ptr_type = self.ConvertTree(tree.type))

  def ConvertArraydecl(self, tree):
    # TODO(spranesh): Handle array dimensions.
    """ Returns Type Object """
    return T.Array(array_type = self.ConvertTree(tree.type))

  def ConvertNonetype(self, tree):
    """ Handle cases when children are none."""
    return None

  def ConvertFuncdecl(self, tree):
    """ Handle Function Declarations."""
    try:
      arguments = map(self.ConvertTree, tree.args.params)
    except AttributeError, e:
      arguments = []

    return N.DeclareFunction(
        position = GetCoords(tree),
        name = None,
        arguments = arguments,
        return_type = self.ConvertTree(tree.type))

  def ConvertFuncdef(self, tree):
    """ Handle Function Declarations. Consists of body, and decl.
        body is a compound statement, and decl is a Declaration."""
    #TODO(spranesh): Handle param_decls, (K&R style of arguments)
    # int main(a)
    # char a;
    func_decl = self.ConvertTree(tree.decl)
    body = self.ConvertTree(tree.body)
    return N.DefineFunction(position = GetCoords(tree),
        name = func_decl.name,
        arguments = func_decl.arguments,
        body = body,
        return_type = func_decl.return_type,
        storage = func_decl.storage,
        quals = func_decl.quals)

  def ConvertCompound(self, tree):
    # The Case Node is screwed up. We need to flesh out the
    # case node's stmt, and put it up one level higher.
    compound_items = []
    for t in tree.block_items:
      ct = self.ConvertTree(t)
      compound_items.append(ct)

      # We could have a case of case of case of ...
      while isinstance(ct, N.CaseDefault):
        t = t.stmt
        ct = self.ConvertTree(t)
        compound_items.append(ct)

    return N.Compound(position = GetCoords(tree),
        compound_items = compound_items)

  def ConvertBinaryop(self, tree):
    assert(tree.op in BINARY_OPERATOR_CONVERSIONS)
    return N.Expression(position = GetCoords(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[tree.op],
        children = map(self.ConvertTree, [tree.left, tree.right]))
    
  def ConvertUnaryop(self, tree):
    assert(tree.op in UNARY_OPERATOR_CONVERSIONS)
    return N.Expression(position = GetCoords(tree),
        operator = UNARY_OPERATOR_CONVERSIONS[tree.op],
        children = map(self.ConvertTree, [tree.expr]))

  def ConvertAssignment(self, tree):
    op = tree.op
    if len(op) is not 1:
      aux_op = op[:-1]
      #TODO(spranesh): Not make any transformations to the += like operators?
      assert(aux_op in BINARY_OPERATOR_CONVERSIONS)

      rvalue = N.Expression(position = GetCoords(tree.rvalue),
          operator = BINARY_OPERATOR_CONVERSIONS[aux_op],
          children = map(self.ConvertTree, [tree.lvalue, tree.rvalue]))
    else:
      rvalue = self.ConvertTree(tree.rvalue)

    return N.Assignment(position = GetCoords(tree),
          lvalue = self.ConvertTree(tree.lvalue),
          rvalue = rvalue)

  def ConvertFunccall(self, tree):
    return N.CallFunction(position = GetCoords(tree),
        function = self.ConvertTree(tree.name),
        arguments = map(self.ConvertTree, tree.args.exprs))

  def ConvertStruct(self, tree):
    # If the pycparser's structure's decls is None, 
    #     the structure is being referred to.
    # Else
    #     it is a structure declaration.
    # TODO(spranesh): Is pyparser a crazy hack or is something wrong with my
    # understanding?
    if tree.decls is None:
      return T.StructureType(structure_type = tree.name)
    else:
      return N.Structure(position = GetCoords(tree),
          name = tree.name,
          members = map(self.ConvertTree, tree.decls))
         
  def ConvertStructref(self, tree):
    op = tree.type  # a.b or a->b
    assert(op in BINARY_OPERATOR_CONVERSIONS)
    return N.Expression(position = GetCoords(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[op],
        children = map(self.ConvertTree, [tree.name, tree.field]))

  def ConvertIf(self, tree):
    return N.IfElse(position = GetCoords(tree),
        condition = self.ConvertTree(tree.cond),
        if_true = self.ConvertTree(tree.iftrue),
        if_false = self.ConvertTree(tree.iffalse))

  def ConvertFor(self, tree):
    return N.For(position = GetCoords(tree),
        init = self.ConvertTree(tree.init),
        condition = self.ConvertTree(tree.cond),
        step = self.ConvertTree(tree.next),
        body = self.ConvertTree(tree.stmt))

  def ConvertWhile(self, tree):
    return N.While(position = GetCoords(tree),
        condition = self.ConvertTree(tree.cond),
        body = self.ConvertTree(tree.stmt))

  def ConvertDowhile(self, tree):
    return N.While(position = GetCoords(tree),
        condition = self.ConvertTree(tree.cond),
        body = self.ConvertTree(tree.stmt),
        do_while = True)

  def ConvertSwitch(self, tree):
    return N.Switch(position = GetCoords(tree),
        switch_on = self.ConvertTree(tree.cond),
        body = self.ConvertTree(tree.stmt))

  def ConvertCase(self, tree):
    return N.CaseDefault(position = GetCoords(tree),
        condition = self.ConvertTree(tree.expr))
    # Condition is None => default

  def ConvertDefault(self, tree):
    return N.CaseDefault(position = GetCoords(tree))

  def ConvertCast(self, tree):
    return N.Expression(position = None,
        operator = 'TYPE_CAST',
        children = [self.ConvertTree(tree.to_type).type,
                    self.ConvertTree(tree.expr)])

  def ConvertTypedef(self, tree):
    return N.DefineType(position = GetCoords(tree),
        name = tree.name,
        type = self.ConvertTree(tree.type))

  def ConvertExprlist(self, tree):
    return N.List(position = GetCoords(tree),
        values = map(self.ConvertTree, tree.exprs))

