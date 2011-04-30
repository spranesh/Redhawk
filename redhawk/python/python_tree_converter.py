#!/usr/bin/env python
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
    NP.NodePosition(self.filename, c.lineno, c.col_offset)



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
        value = str(tree.s),
        type = T.BaseType('string'))


  def ConvertBinop(self, tree):
    """ Convert the BinOp(expr left, operator op, expr right) node.

      op\ in  Add | Sub | Mult | Div | Mod | Pow | LShift | RShift | BitOr
            | BitXor | BitAnd | FloorDiv"""
    return N.Expression(position = self.gc.GC(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = map(self.ConvertTree, [tree.left, tree.right]))


  def ConvertName(self, tree):
    if isinstance(tree.ctx, ast.Param):
      return N.DefineVariable(self.gc.GC(tree),
          name = tree.id)
    return N.ReferVariable(self.gc.GC(tree),
        name = tree.id)


  def ConvertBoolop(self, tree):
    """ Convert the BoolOp(boolop op, expr* values) node. (And | Or) """
    return N.Expression(position = self.gc.GC(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = map(self.ConvertTree, tree.values))


  def __ConvertBinaryOperation(self, op, position, left, right):
    """ We split the conversion into two cases - not in, is not (not
    operators), and the rest. In the not operators case, we use the
    NOT_BINARY_OPERATORS dictionary, and a BOOLEAN_NOT."""
    expr = N.Expression(position = position,
        operator = None,
        children = map(self.ConvertTree, [left, right]))

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
        members = map(self.ConvertTree, tree.elts))


  def ConvertList(self, tree):
    """ Convert the List(expr* elts, expr_context ctx) node."""
    return N.List(position = self.gc.GC(tree),
        values = map(self.ConvertTree, tree.elts))
 

  def ConvertAssign(self, tree):
    """ Convert the Assign(expr* targets, expr value) node."""
    if len(tree.targets) > 1:
      left = N.Tuple(position = self.gc.GC(tree.targets),
          members = map(self.ConvertTree, tree.targets))
    else:
      left = self.ConvertTree(tree.targets[0])

    return N.Assignment(position = self.gc.GC(tree),
        lvalue = left,
        rvalue = self.ConvertTree(tree.value))


  def ConvertAugassign(self, tree):
    """ Convert the AugAssign(expr target, operator op, expr value) node."""
    #TODO(spranesh): Not cheat?
    rvalue = N.Expression(position = self.gc.GC(tree.value),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = map(self.ConvertTree, [tree.target, tree.value]))

    return N.Assignment(position = self.gc.GC(tree),
        lvalue = self.ConvertTree(tree.target),
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
        if_true =  self.ConvertCompound(tree.body),
        if_false = self.ConvertCompound(tree.orelse))


  def ConvertIfexp(self, tree):
    """ Convert the IfExp(expr test, expr body, expr orelse) node."""
    return N.Expression(position = self.gc.GC(tree),
        operator = 'TERNARY_IF',
        children = map(self.ConvertTree, [tree.test, tree.body,
          tree.orelse]))


  def ConvertCompound(self, li):
    """ Convert a list of statements into a compound node. """
    assert(type(li) == list)

    return N.Compound(position = self.gc.GC(li[0]),
        compound_items = map(self.ConvertTree, li))


  def ConvertModule(self, tree):
    return N.Module(self.filename,
        children = map(self.ConvertTree, tree.body))


  def ConvertInteractive(self, tree):
    return N.Module(None,
        children = map(self.ConvertTree, tree.body))


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
        children = map(self.ConvertTree, tree.ifs))

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
        generators = map(self.ConvertTree, tree.generators))


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
    body_node = N.Compound(position = self.gc.GC(tree),
                      compound_items = map(self.ConvertTree, tree.body))

    f = N.DefineFunction(position = self.gc.GC(tree),
                            name = tree.name,
                            arguments = argument_node,
                            body = body_node)
    
    # Encapsulate in decorators
    current = f
    for d in tree.decorator_list[::-1]:
      current = N.FunctionDecorator(position = self.gc.GC(d),
                                    decorator = self.ConvertTree(d),
                                    function = current)
    return current
      

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
      arguments.append(N.DefineVariable(position = self.gc.GC(tree.args[-1]),
                                        name = k.arg,
                                        init = self.ConvertTree(k.value)))

    argument_node = N.FunctionArguments(position = self.gc.GC(tree.args[0]),
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
                     body = map(self.ConvertTree, tree.body))

  def ConvertWhile(self, tree):
    """ Convert

      While(expr test, stmt* body, stmt* orelse)

    into the While node."""
    return N.While(position = self.gc.GC(tree),
                   condition = self.ConvertTree(tree.test),
                   body = map(self.ConvertTree, tree.body))

 
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
                    targets = map(self.ConvertTree, tree.targets))

  def ConvertPrint(self, tree):
    """ Convert the Print(expr? dest, expr* values, bool nl)
      statement.
    """
    # TODO(spranesh): We currently ignore nl
    return N.Print(position = self.gc.GC(tree),
                   values = map(self.ConvertTree, tree.values),
                   stream = self.ConvertTree(tree.dest))


  def ConvertRaise(self, tree):
    """ Convert the Raise(expr? type, expr? inst, expr? tback)"""
    #TODO(spranesh): We currently ignore inst, and tback
    return N.Raise(position = self.gc.GC(tree),
                   exception_type = self.ConvertTree(tree.type))


  def ConvertExcepthandler(self, tree):
    """ Convert the ExceptHandler(expr? type, expr? name, stmt* body) node."""
    return N.ExceptionHandler(position = self.gc.GC(tree),
                              body = map(self.ConvertTree, tree.body),
                              name = self.ConvertTree(tree.name),
                              type = self.ConvertTree(tree.type))


  def ConvertTryexcept(self, tree):
    """ Convert the 
    TryExcept(stmt* body, excepthandler* handlers, stmt* orelse)
    node. """
    return N.TryCatch(position = self.gc.GC(tree),
                      body = map(self.ConvertTree, tree.body),
                      exception_handlers = map(self.ConvertTree, tree.handlers),
                      orelse = map(self.ConvertTree, tree.orelse))


  def ConvertTryFinally(self, tree):
    """ Convert the | TryFinally(stmt* body, stmt* finalbody) node."""
    pass
