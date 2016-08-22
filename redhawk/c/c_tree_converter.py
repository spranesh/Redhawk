#!/usr/bin/env python
""" Convert C-Tree to ast. """

from __future__ import absolute_import
import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.traverse as traverse
import redhawk.common.tree_converter as tree_converter
import redhawk.common.type as T
import redhawk.utils.util as U
import logging

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
  if c is None:
    logging.debug('%s does not have a coordinate'%(t))
    return None
  return NP.NodePosition(c.file, c.line, c.column)

class CTreeConverter(tree_converter.TreeConverter):
  def Convert(self, tree):
    """ Override the convert method in the base class to handle escape
    character representation by cpyparser."""
    l_ast = tree_converter.TreeConverter.Convert(self, tree)
    self.UnescapeEscapeCharacters(l_ast)
    return l_ast

  def UnescapeEscapeCharacters(self, tree):
    """ Cpyparser stores new lines as \\n, so that when printed they appear as
    \n. We want to unescape these newlines (and tabs), to match what python's
    ast module does."""
    for node in traverse.DFS(tree):
      for attr in node.GetAttributes()[1]:
        value = getattr(node, attr)
        if type(value) is str:
          unescaped_string = (value.replace("\\n", "\n").replace("\\t",
              "\t").replace("\'", "").replace("\"", ""))
          setattr(node, attr, unescaped_string)
    return

  def ConvertFileast(self, tree):
    return N.Module(position = NP.NodePosition(self.filename, 1, 1),
        filename = self.filename,
        children = self.ConvertListOfStatements(tree.children()))

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
    if isinstance(t, N.Enumerator):
      t.storage, t.quals = None, None
      return t
    if isinstance(t, N.Union):
      t.storage, t.quals = None, None
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
    except IndexError as e:
      # Default type is int in C
      return T.BaseType(base_type = 'int')

  def ConvertTypedecl(self, tree):
    """ Returns Type Object """
    # child is either an IdentifierType or a Struct
    t = self.ConvertTree(tree.type)
    assert(isinstance(t, T.BaseType)
        or isinstance(t, T.EnumeratorType)
        or isinstance(t, T.StructureType)
        or isinstance(t, T.UnionType)
        or isinstance(t, N.Enumerator)
        or isinstance(t, N.Structure)
        or isinstance(t, N.Union))
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

  def ConvertParamlist(self, tree):
    """ Handle Function Arguments.
        In case the last is an ellipsis param, we store it as a var_arg
        of name va_list."""
    try:
      position = GetCoords(tree)
    except AssertionError as e:
      position = None

    #TODO(spranesh): Cheap Hack?
    if tree.params[-1].__class__.__name__ == 'EllipsisParam':
      try:
        va_list_position = GetCoords(tree.params[-1])
      except AssertionError as e:
        va_list_position = None

      return N.FunctionArguments(position = position,
          arguments = self.ConvertListOfStatements(tree.params[:-1]),
          var_arguments = [N.DefineVariable(va_list_position, 'va_list')])

    return N.FunctionArguments(position = position,
         arguments = self.ConvertListOfStatements(tree.params))

  def ConvertFuncdecl(self, tree):
    """ Handle Function Declarations."""
    if tree.args:
      arguments = self.ConvertTree(tree.args)
    else:
      arguments = N.FunctionArguments(position = None, arguments = [])

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
    """ Note that this function returns a list, as opposed to a node."""
    # The Case Node is screwed up. We need to flesh out the
    # case node's stmt, and put it up one level higher.
    if not tree.block_items:
      return []

    compound_items = []
    for t in tree.block_items:
      ct = self.ConvertTree(t)
      compound_items.append(ct)

      # We could have a case of case of case of ...
      while isinstance(ct, N.CaseDefault):
        t = t.stmt
        ct = self.ConvertTree(t)
        compound_items.append(ct)

    # We should be using self.ConvertListOfStatements here,
    # but since the converted nodes are already in a list,
    # we return that.
    return compound_items

  def ConvertBinaryop(self, tree):
    assert(tree.op in BINARY_OPERATOR_CONVERSIONS)
    return N.Expression(position = GetCoords(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[tree.op],
        children = self.ConvertListOfStatements([tree.left, tree.right]))

  def ConvertUnaryop(self, tree):
    assert(tree.op in UNARY_OPERATOR_CONVERSIONS)
    return N.Expression(position = GetCoords(tree),
        operator = UNARY_OPERATOR_CONVERSIONS[tree.op],
        children = self.ConvertListOfStatements([tree.expr]))

  def ConvertAssignment(self, tree):
    op = tree.op
    if len(op) is not 1:
      aux_op = op[:-1]
      #TODO(spranesh): Not make any transformations to the += like operators?
      assert(aux_op in BINARY_OPERATOR_CONVERSIONS)

      # Make sure that the same subtree is there in both the lvalue,
      # and the first child of the rvalue
      lvalue = self.ConvertTree(tree.lvalue)
      rvalue = N.Expression(position = GetCoords(tree.rvalue),
          operator = BINARY_OPERATOR_CONVERSIONS[aux_op],
          children = [lvalue, self.ConvertTree(tree.rvalue)])
    else:
      lvalue = self.ConvertTree(tree.lvalue)
      rvalue = self.ConvertTree(tree.rvalue)

    return N.Assignment(position = GetCoords(tree),
          lvalue = lvalue,
          rvalue = rvalue)

  def ConvertFunccall(self, tree):
    arguments = []
    if tree.args:
      arguments = self.ConvertListOfStatements(tree.args.exprs)

    return N.CallFunction(position = GetCoords(tree),
        function = self.ConvertTree(tree.name),
        arguments = N.FunctionArguments(position = GetCoords(tree),
          arguments = arguments))

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
          members = self.ConvertListOfStatements(tree.decls))

  def ConvertStructref(self, tree):
    op = tree.type  # a.b or a->b
    assert(op in BINARY_OPERATOR_CONVERSIONS)
    return N.Expression(position = GetCoords(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[op],
        children = self.ConvertListOfStatements([tree.name, tree.field]))

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
        values = self.ConvertListOfStatements(tree.exprs))

  def ConvertArrayref(self, tree):
    return N.Expression(position = GetCoords(tree),
        operator = 'INDEX_INTO',
        children = [self.ConvertTree(tree.name),
                    self.ConvertTree(tree.subscript)])

  def ConvertEnum(self, tree):
    # If the pycparser's Enum's values is empty:
    #     the enumerator is being referred to.
    # Else
    #     it is a enumerator declaration.
    # A crazy pycparser hack
    if tree.values is None:
      return T.EnumeratorType(enumerator_type = tree.name)
    else:
      return N.Enumerator(position = GetCoords(tree),
          name = tree.name,
          values = self.ConvertListOfStatements(tree.values.enumerators))

  def ConvertEnumerator(self, tree):
    return N.DeclareSymbol(position = GetCoords(tree),
        name = tree.name,
        value = self.ConvertTree(tree.value))

  def ConvertContinue(self, tree):
    return N.Continue(position = GetCoords(tree))

  def ConvertBreak(self, tree):
    return N.Break(position = GetCoords(tree))

  def ConvertGoto(self, tree):
    return N.Goto(position = GetCoords(tree),
        location = tree.name)

  def ConvertLabel(self, tree):
    return N.SourceLabel(position = GetCoords(tree),
        name = tree.name,
        statements = [self.ConvertTree(tree.stmt)])

  def ConvertTuple(self, tree):
    # pycparser often returns nodes of the form:
    # ('edge', node) where edge is a string that denotes
    # the path taken down. In such a case, we want to
    # ignore the string, and simply convert the node.
    self.Convert(tree[1])
    return

  def ConvertUnion(self, tree):
    # If the pycparser's union's decls is empty:
    #     the union is being referred to.
    # Else
    #     it is a union declaration.
    # A crazy pyparser hack
    if tree.decls is None:
      return T.UnionType(union_type = tree.name)
    else:
      return N.Union(position = GetCoords(tree),
          name = tree.name,
          members = self.ConvertListOfStatements(tree.decls))

  def ConvertTernaryop(self, tree):
    return N.Expression(position = GetCoords(tree),
        operator = 'TERNARY_IF',
        children = self.ConvertListOfStatements([tree.cond, tree.iftrue,
          tree.iffalse]))
