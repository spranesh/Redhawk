#!/usr/bin/env python
from __future__ import absolute_import
import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.tree_converter as tree_converter
import redhawk.common.types as T

import ast

# Map Python AST operators into the L-AST operators
# Add | Sub | Mult | Div | Mod | Pow | LShift
#                  | RShift | BitOr | BitXor | BitAnd | FloorDiv
#
# Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
# And | Or
BINARY_OPERATOR_CONVERSIONS = {
      'Add'       : 'ADD'
     ,'Sub'       : 'MINUS'
     ,'Mult'      : 'MULTIPLY'
     ,'Div'       : 'DIVIDE'
     ,'Pow'       : 'POWER'
     ,'BitXor'    : 'BITWISE_XOR'
     ,'BitOr'     : 'BITWISE_OR'
     ,'BitAnd'    : 'BITWISE_AND'
     ,'LShift'    : 'LSHIFT'
     ,'RShift'    : 'RSHIFT'
     ,'Mod'       : 'MOD'
     ,'FloorDiv'  : 'FLOOR_DIVIDE'
     ,'Lt'        : 'LT'
     ,'Gt'        : 'GT'
     ,'LtE'       : 'LTE'
     ,'GtE'       : 'GTE'
     ,'Eq'        : 'EQ'
     ,'NotEq'     : 'NOT_EQ'
     ,'And'       : 'BOOLEAN_AND'
     ,'Or'        : 'BOOLEAN_OR'
     ,'Is'        : 'IS'
     ,'In'        : 'IN'
     # ,'.'       : 'ATTRIBUTE_INDEX'
     # ,'->'      : 'ARROW' # TODO(spranesh): Bad Name?
}

NOT_BINARY_OPERATORS = {
      'NotIn'       : 'IN'
     ,'IsNot'       : 'IS'
}

# Invert | Not | UAdd | USub
UNARY_OPERATOR_CONVERSIONS = {
      'Invert' : 'BITWISE_NOT'
     ,'Not'    : 'BOOLEAN_NOT'
     ,'UAdd'   : 'UNARY_PLUS'
     ,'USub'   : 'UNARY_MINUS'
}


class TransformCoord:
  """ A class to help transform coordinates from the python ast to the L-AST.
  This has been made a class, because it has state."""
  def __init__(self, filename):
    self.filename = filename
    return


  def GC(self, c):
    """ Get Coord."""
    try:
      return NP.NodePosition(self.filename, c.lineno, c.col_offset)
    except AttributeError as e:
      return None


def GetClassName(x):
  return x.__class__.__name__



class PythonTreeConverter(tree_converter.TreeConverter):
  def __init__(self, filename=None):
    tree_converter.TreeConverter.__init__(self, filename)
    self.gc = TransformCoord(filename)
    return


  def ConvertNonetype(self, tree):
    return None


  def ConvertExpr(self, tree):
    return self.ConvertTree(tree.value)


  def ConvertNum(self, tree):
    #TODO(spranesh): Should the value be really str-ed?
    return N.Constant(self.gc.GC(tree),
        value = str(tree.n),
        type = T.BaseType('number'))


  def ConvertStr(self, tree):
    #TODO(spranesh): Should the value be really str-ed?
    return N.Constant(self.gc.GC(tree),
        value = tree.s,
        type = T.BaseType('string'))


  def ConvertRepr(self, tree):
    return N.Show(position = self.gc.GC(tree),
        value = self.ConvertTree(tree.value))


  def ConvertExec(self, tree):
    return N.Exec(position = self.gc.GC(tree),
        body = self.ConvertTree(tree.body),
        locals = self.ConvertTree(tree.locals),
        globals = self.ConvertTree(tree.globals))


  def ConvertBinop(self, tree):
    """ Convert the BinOp(expr left, operator op, expr right) node.

      op\ in  Add | Sub | Mult | Div | Mod | Pow | LShift | RShift | BitOr
            | BitXor | BitAnd | FloorDiv"""
    return N.Expression(position = self.gc.GC(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = list(map(self.ConvertTree, [tree.left, tree.right])))


  def ConvertName(self, tree):
    if isinstance(tree.ctx, ast.Param):
      return N.DefineVariable(self.gc.GC(tree),
          name = tree.id)
    return N.ReferVariable(self.gc.GC(tree),
        name = tree.id)


  def ConvertNameconstant(self, tree):
    # New AST type in Python 3
    # TODO: is this correct?
    return N.ReferVariable(self.gc.GC(tree), name=str(tree.value))


  def ConvertArg(self, tree):
    # New AST type in Python 3
    # TODO: is this correct?
    return N.DefineVariable(self.gc.GC(tree), name=tree.arg)


  def ConvertBoolop(self, tree):
    """ Convert the BoolOp(boolop op, expr* values) node. (And | Or) """
    return N.Expression(position = self.gc.GC(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = list(map(self.ConvertTree, tree.values)))


  def __ConvertBinaryOperation(self, op, position, left, right):
    """ We split the conversion into two cases - not in, is not (not
    operators), and the rest. In the not operators case, we use the
    NOT_BINARY_OPERATORS dictionary, and a BOOLEAN_NOT."""
    expr = N.Expression(position = position,
        operator = None,
        children = list(map(self.ConvertTree, [left, right])))

    if op in NOT_BINARY_OPERATORS:
      expr.operator = NOT_BINARY_OPERATORS[op]
      expr = N.Expression(position = position,
          operator = 'BOOLEAN_NOT',
          children = [expr])

    else:
      expr.operator = BINARY_OPERATOR_CONVERSIONS[op]

    return expr


  def ConvertCompare(self, tree):
    """ Convert the Compare(expr left, cmpop* ops, expr* comparators) node.

    Each of the ops are \in   Eq | NotEq | Lt | LtE | Gt | GtE | Is
                            | IsNot | In | NotIn

    More than one comparison is possible. Like 3 < x < 4.
    If the lenght of ops is one, then we return a simple comparison node, else
    we return an and of comparison nodes."""

    if len(tree.ops) is 1:
      return self.__ConvertBinaryOperation(position = self.gc.GC(tree),
          op = GetClassName(tree.ops[0]),
          left = tree.left,
          right = tree.comparators[0])

    comparisons = []
    comparators = [tree.left] + tree.comparators
    for (i, c) in enumerate(tree.ops):
      comparisons.append(self.__ConvertBinaryOperation(
          position = self.gc.GC(comparators[i]),
          op = GetClassName(c),
          left = comparators[i],
          right = comparators[i+1]))

    return N.Expression(position = self.gc.GC(tree),
        operator = 'BOOLEAN_AND',
        children = comparisons)


  def ConvertUnaryop(self, tree):
    """ Convert the UnaryOp(unaryop op, expr operand) node.
    op \in Invert | Not | UAdd | USub """
    return N.Expression(position = self.gc.GC(tree),
        operator = UNARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = [self.ConvertTree(tree.operand)])


  def ConvertTuple(self, tree):
    """ Convert the Tuple(expr* elts, expr_context ctx) node."""
    return N.Tuple(position = self.gc.GC(tree),
        members = list(map(self.ConvertTree, tree.elts)))


  def ConvertList(self, tree):
    """ Convert the List(expr* elts, expr_context ctx) node."""
    return N.List(position = self.gc.GC(tree),
        values = list(map(self.ConvertTree, tree.elts)))

  def ConvertDict(self, tree):
    """ Convert the Dict(expr* keys, expr* values) node."""
    return N.Dict(position = self.gc.GC(tree),
        keys = list(map(self.ConvertTree, tree.keys)),
        values = list(map(self.ConvertTree, tree.values)))


  def ConvertAssign(self, tree):
    """ Convert the Assign(expr* targets, expr value) node."""
    if len(tree.targets) > 1:
      left = N.Tuple(position = self.gc.GC(tree.targets),
          members = list(map(self.ConvertTree, tree.targets)))
    else:
      left = self.ConvertTree(tree.targets[0])

    return N.Assignment(position = self.gc.GC(tree),
        lvalue = left,
        rvalue = self.ConvertTree(tree.value))


  def ConvertAugassign(self, tree):
    """ Convert the AugAssign(expr target, operator op, expr value) node."""
    #TODO(spranesh): Not cheat?
    lvalue = self.ConvertTree(tree.target)
    rvalue = N.Expression(position = self.gc.GC(tree.value),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = [lvalue, self.ConvertTree(tree.value)])

    return N.Assignment(position = self.gc.GC(tree),
        lvalue = lvalue,
        rvalue = rvalue)


  def ConvertAttribute(self, tree):
    """ Convert the Attribute(expr value, identifier attr, expr_context ctx)
    node."""
    return N.Expression(position = self.gc.GC(tree),
        operator = 'ATTRIBUTE_INDEX',
        children = [self.ConvertTree(tree.value)
                   ,N.ReferVariable(self.gc.GC(tree), tree.attr)])


  def ConvertSlice(self, tree):
    """ Convert the Slice(expr? lower, expr? upper, expr? step) node."""
    return N.Slice(position = None,
                   lower = self.ConvertTree(tree.lower),
                   upper = self.ConvertTree(tree.upper),
                   step =  self.ConvertTree(tree.step))


  def ConvertExtslice(self, tree):
    """ Convert ExtSlice(slice *dims)."""
    #TODO(spranesh): Cheap hack. We only convert the first slice.
    #Maybe use a compound?
    return self.ConvertTree(tree.dims[0])


  def ConvertIndex(self, tree):
    """ Convert the Index(expr value) node."""
    return self.ConvertTree(tree.value)


  def ConvertSubscript(self, tree):
    """ Convert Subscript(expr value, slice slice, expr_context ctx) node."""
    return N.Expression(position = self.gc.GC(tree),
        operator = 'INDEX_INTO',
        children = [self.ConvertTree(tree.value),
                    self.ConvertTree(tree.slice)])


  def ConvertIf(self, tree):
    """ Convert the If(expr test, expr body, expr orelse) node."""
    return N.IfElse(position = self.gc.GC(tree),
        condition = self.ConvertTree(tree.test),
        if_true =  self.ConvertListOfStatements(tree.body),
        if_false = self.ConvertListOfStatements(tree.orelse))


  def ConvertIfexp(self, tree):
    """ Convert the IfExp(expr test, expr body, expr orelse) node."""
    return N.Expression(position = self.gc.GC(tree),
        operator = 'TERNARY_IF',
        children = list(map(self.ConvertTree, [tree.test, tree.body,
          tree.orelse])))


  def ConvertCompound(self, li):
    """ Convert a list of statements into a compound node. """
    assert(type(li) == list)
    if len(li) == 0:
      return None

    return N.Compound(position = self.gc.GC(li[0]),
        compound_items = list(map(self.ConvertTree, li)))


  def ConvertModule(self, tree):
    return N.Module(position = NP.NodePosition(self.filename, 1, 1),
        filename = self.filename,
        children = list(map(self.ConvertTree, tree.body)))


  def ConvertInteractive(self, tree):
    return N.Module(None,
        children = list(map(self.ConvertTree, tree.body)))


  def ConvertExpression(self, tree):
    return self.ConvertInteractive(tree)


  def ConvertComprehension(self, tree):
    """ Convert the comprehension(expr target, expr iter, expr* ifs) node into
    a Generator.

    Note that the ifs must be combined into a single condition."""

    condition = None
    if tree.ifs != []:
      condition = N.Expression(position = self.gc.GC(tree.ifs[0]),
        operator = 'BOOLEAN_AND',
        children = list(map(self.ConvertTree, tree.ifs)))

    return N.Generator(position = None,
        target = self.ConvertTree(tree.target),
        generator = self.ConvertTree(tree.iter),
        condition = condition)


  def __ConvertXComprehension(self, tree, elt, type):
    """ Convert a comprehension of type elt, whose LHS can be expressed as the
    converted expression elt.

    (A helper function for ConvertListComprehension, ConvertDictComprehension,
    and ConvertSetComprehension.)"""

    return N.Comprehension(position = self.gc.GC(tree),
        expr = elt,
        type = type,
        generators = list(map(self.ConvertTree, tree.generators)))


  def ConvertListcomp(self, tree):
    """ Conver the ListComp(expr elt, comprehension* generators) node.
    Type is 'list'."""

    return self.__ConvertXComprehension(tree,
        elt = self.ConvertTree(tree.elt),
        type = 'list')


  def ConvertGeneratorexp(self, tree):
    return self.__ConvertXComprehension(tree,
        elt = self.ConvertTree(tree.elt),
        type = 'generator')


  # Python 3
  def ConvertSetcomp(self, tree):
    """ Convert the SetComp(expr elt, comprehension* generators) node.
    Type is 'set'."""

    return self.__ConvertXComprehension(tree,
        elt = self.ConvertTree(tree.elt),
        type = 'set')


  # Python 3
  def ConvertDictcomp(self, tree):
    """ Convert the DictComp(expr key, expr value, comprehension* generators)
    node.

    Type is 'dict'.

    The value is stored as a pair expression."""
    elt = N.Tuple(position = self.gc.GC(tree),
        members = [self.ConvertTree(tree.key)
                  ,self.ConvertTree(tree.value)])

    return self.__ConvertXComprehension(tree,
        elt = elt,
        type = 'dict')


  def __ConvertArguments(self, args, position):
    """ Convert the Python argument node to the FunctionArguments L-AST node. The
    arguments need to be variable definitions, which do not exist elsewhere in
    Python (everything else is a ReferVariable).  We therefore handle it here
    itself. """

    arguments =  []
    for x in args.args:
      arguments.append(self.ConvertTree(x))


    for (i, y) in enumerate(args.defaults):
      arguments[len(arguments) - len(args.defaults) + i].init = self.ConvertTree(y)

    vararg, kwarg = None, None
    if args.vararg:
      vararg = N.DefineVariable(position = position, name = args.vararg)
    if args.kwarg:
      kwarg = N.DefineVariable(position = position, name = args.kwarg)


    return N.FunctionArguments(position = position,
                               arguments = arguments,
                               var_arguments = vararg,
                               kwd_arguments = kwarg)


  def ConvertFunctiondef(self, tree):
    """ Convert the FunctionDef node.
        FunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list)

        arguments = (expr* args, identifier? vararg, identifier? kwarg, expr*
        defaults)

        position, name, arguments, body
        """


    argument_node = self.__ConvertArguments(tree.args, self.gc.GC(tree))
    # Convert body
    body_node = self.ConvertListOfStatements(tree.body)

    f = N.DefineFunction(position = self.gc.GC(tree),
                            name = tree.name,
                            arguments = argument_node,
                            body = body_node)


    return self.__EncapsulateNodeInDecorators(f, tree.decorator_list[::-1])


  def __EncapsulateNodeInDecorators(self, node, decorator_list):
    """ Encapsulate `node` in decorators from `decorator_list`"""
    for d in decorator_list[::-1]:
      node = N.FunctionDecorator(position = self.gc.GC(d),
                                    decorator = self.ConvertTree(d),
                                    function = node)
    return node


  def ConvertCall(self, tree):
    """ Convert a function call:

      Call(expr func, expr* args, keyword* keywords, expr? starargs, expr? kwargs)
      keyword = (identifier arg, expr value)

      into
      CallFunction: position, function, arguments """

    # Set up the arguments, using args, keywords, starargs, kwargs
    arguments = []
    for a in tree.args:

      arguments.append(self.ConvertTree(a))

    for k in tree.keywords:
      position_reference = tree.args[-1] if len(tree.args) > 0 else tree
      arguments.append(N.DefineVariable(position = self.gc.GC(position_reference),
                                        name = k.arg,
                                        init = self.ConvertTree(k.value)))


    argument_node = N.FunctionArguments(position = self.gc.GC(tree.args[0]) if len(tree.args) > 0 else None,
                                        arguments = arguments,
                                        var_arguments = self.ConvertTree(tree.starargs),
                                        kwd_arguments = self.ConvertTree(tree.kwargs))


    return N.CallFunction(position = self.gc.GC(tree),
                          function = self.ConvertTree(tree.func),
                          arguments = argument_node)


  def ConvertLambda(self, tree):
    """ Convert the lamdba function:
        Lambda(arguments args, expr body)

        into
        Lambda: position, arguments, value"""
    argument_node = self.__ConvertArguments(tree.args, self.gc.GC(tree))

    return N.Lambda(position = self.gc.GC(tree),
                    arguments = argument_node,
                    value = self.ConvertTree(tree.body))

  def ConvertFor(self, tree):
    """ Convert

    For(expr target, expr iter, stmt* body, stmt* orelse)

    into the ForEach L-ASt node."""

    # TODO(spranesh): The target must be a DefineVariable rather than a ReferVariable.
    # So give it a context of Param(). (ConvertName will handle the rest).
    define_target_node = self.ConvertTree(tree.target)

    return N.ForEach(position = self.gc.GC(tree),
                     target = define_target_node,
                     iter_expression = self.ConvertTree(tree.iter),
                     body = self.ConvertListOfStatements(tree.body))

  def ConvertWhile(self, tree):
    """ Convert

      While(expr test, stmt* body, stmt* orelse)

    into the While node."""
    return N.While(position = self.gc.GC(tree),
                   condition = self.ConvertTree(tree.test),
                   body = self.ConvertListOfStatements(tree.body))


  def ConvertBreak(self, tree):
    """ Convert the Continue statement. (Duh?)"""
    return N.Break(position = self.gc.GC(tree))


  def ConvertContinue(self, tree):
    """ Convert the Continue statement. (Like, Duh?)"""
    return N.Continue(position = self.gc.GC(tree))


  def ConvertPass(self, tree):
    """ Convert the Pass statement. (Like, Duh-uh?)"""
    return N.Pass(position = self.gc.GC(tree))


  def ConvertAssert(self, tree):
    """ Convert Assert(expr test, expr? msg) """
    return N.Assert(position = self.gc.GC(tree),
                    test_expression = self.ConvertTree(tree.test),
                    message = self.ConvertTree(tree.msg))


  def ConvertDelete(self, tree):
    """ Convert the Delete(expr* targets) statement."""
    return N.Delete(position = self.gc.GC(tree),
                    targets = list(map(self.ConvertTree, tree.targets)))

  def ConvertPrint(self, tree):
    """ Convert the Print(expr? dest, expr* values, bool nl)
      statement.
    """
    # TODO(spranesh): We currently ignore nl
    return N.Print(position = self.gc.GC(tree),
                   values = list(map(self.ConvertTree, tree.values)),
                   stream = self.ConvertTree(tree.dest))


  def ConvertRaise(self, tree):
    """ Convert the Raise(expr? type, expr? inst, expr? tback)"""
    #TODO(spranesh): We currently ignore inst, and tback
    # in Python 2, it's tree.type, in Python 3 it's tree.exc
    tp = tree.type if hasattr(tree, 'type') else tree.exc
    return N.Raise(position = self.gc.GC(tree),
                   exception_type = self.ConvertTree(tp))


  def ConvertExcepthandler(self, tree):
    """ Convert the ExceptHandler(expr? type, expr? name, stmt* body) node."""
    if isinstance(tree.name, str):
        # in Python 3, tree.name is string
        name = N.DefineVariable(position=self.gc.GC(tree), name=tree.name)
    else:
        name = self.ConvertTree(tree.name)
    return N.ExceptionHandler(position = self.gc.GC(tree),
                              body = self.ConvertListOfStatements(tree.body),
                              name = name,
                              type = self.ConvertTree(tree.type))


  def ConvertTryexcept(self, tree):
    """ Convert the
    TryExcept(stmt* body, excepthandler* handlers, stmt* orelse)
    node. """
    return N.TryCatch(position = self.gc.GC(tree),
                      body = self.ConvertListOfStatements(tree.body),
                      exception_handlers = list(map(self.ConvertTree, tree.handlers)),
                      orelse = self.ConvertListOfStatements(tree.orelse))


  def ConvertTryfinally(self, tree):
    """ Convert the | TryFinally(stmt* body, stmt* finalbody) node."""
    return N.Finally(position = self.gc.GC(tree),
                     body = self.ConvertListOfStatements(tree.body),
                     final_body = self.ConvertListOfStatements(tree.finalbody))

  def ConvertTry(self, tree):
    # New AST type in Python 3
    # TODO: is this correct?
    return N.Try(position=self.gc.GC(tree),
                 body = self.ConvertListOfStatements(tree.body),
                 exception_handlers = list(map(self.ConvertTree, tree.handlers)),
                 orelse = self.ConvertListOfStatements(tree.orelse),
                 final_body = self.ConvertListOfStatements(tree.finalbody))

  def ConvertWith(self, tree):
    """ Convert With(expr context_expr, expr? optional_vars, stmt* body) node."""
    if hasattr(tree, 'optional_vars'):
      # Python 2 -> if there are more assignments, multiple nested with statements are created
      assign_node = ast.Assign(
        [tree.optional_vars],
        tree.context_expr,
        lineno = tree.lineno,
        col_offset = tree.col_offset)
    else:
      # Python 3 -> no nested with statements, everything at once
      targets = []
      values = []
      for item in tree.items:
        targets.append(item.optional_vars)
        values.append(item.context_expr)
      targets = ast.Tuple(elts=targets, lineno=tree.lineno, col_offset=tree.col_offset)
      values = ast.Tuple(elts=values, lineno=tree.lineno, col_offset=tree.col_offset)
      assign_node = ast.Assign([targets], values, lineno=tree.lineno, col_offset=tree.col_offset)

    defvars = [self.ConvertTree(assign_node)]
    return N.Let(position = self.gc.GC(tree),
                 defvars = defvars,
                 body = self.ConvertListOfStatements(tree.body))

  def ConvertClassdef(self, tree):
    """ Convert the
      ClassDef(identifier name, expr* bases, stmt* body, expr* decorator_list)
    node."""

    c = N.DefineClass(position = self.gc.GC(tree),
                      name = tree.name,
                      inherits = list(map(self.ConvertTree, tree.bases)),
                      body = list(map(self.ConvertTree, tree.body)))

    return self.__EncapsulateNodeInDecorators(c, tree.decorator_list[::-1])

  def ConvertAlias(self, tree):
    """ Convert alias = (identifier name, identifier? asname)"""
    return N.ModuleAlias(position = None,
                         name = tree.name,
                         asmodule = tree.asname)

  def ConvertImport(self, tree):
    """ Convert Import(alias* names) node."""
    return N.Import(position = self.gc.GC(tree),
                    import_aliases = list(map(self.ConvertAlias, tree.names)))

  def ConvertImportfrom(self, tree):
    """ Convert the
      ImportFrom(identifier? module, alias* names, int? level)
    node."""
    return N.ImportFrom(position = self.gc.GC(tree),
                        module = tree.module,
                        import_aliases = list(map(self.ConvertAlias, tree.names)))

  def ConvertGlobal(self, tree):
    return N.ContextVariables(position = self.gc.GC(tree),
                     names = tree.names,
                     context = 'globals')

  def ConvertReturn(self, tree):
    return N.Return(position = self.gc.GC(tree),
                    return_expression = self.ConvertTree(tree.value))

  def ConvertYield(self, tree):
    return N.Yield(position = self.gc.GC(tree),
                    yield_expression = self.ConvertTree(tree.value))
