""" Node Classes.

    This file is AUTO GENERATED from
      node_cfg.yaml using _ast_gen.py
    The header is stored in node_header.py
"""

import writers.scheme_writer as S
import redhawk.utils.util as U

import copy
import pprint

# -1 means infinite number of operators possible
# A dictionary of allowed operators, and their arity.
ALLOWED_OPERATORS = {
     'UNARY_MINUS'         : ('-', 1)
    ,'UNARY_PLUS'          : ('+', 1)
    ,'SIZE_OR_LEN'         : ('size-or-len-of', 1)

    ,'MULTIPLY'            : ('*', -1)
    ,'ADD'                 : ('+', -1)
    ,'MINUS'               : ('-', 2)
    ,'DIVIDE'              : ('/', 2)
    ,'FLOOR_DIVIDE'        : ('//', 2)
    ,'POWER'               : ('power', 2)
    ,'MOD'                 : ('mod', 2)
    ,'LSHIFT'              : ('lshift', 2)
    ,'RSHIFT'              : ('rshift', 2)
    ,'BITWISE_OR'          : ('bitwise-or', 2)
    ,'BITWISE_XOR'         : ('bitwise-xor', 2)
    ,'BITWISE_AND'         : ('bitwise-and', 2)
    ,'BITWISE_NOT'         : ('bitwise-not', 1)

    ,'BOOLEAN_AND'         : ('and', -1)
    ,'BOOLEAN_OR'          : ('or',  -1)
    ,'BOOLEAN_NOT'         : ('not', 1)
    ,'EQ'                  : ('eq', 2)
    ,'NOT_EQ'              : ('not-eq', 2)
    ,'IS'                  : ('is', 2)
    ,'IN'                  : ('in', 2)
    ,'LT'                  : ('<', 2)
    ,'LTE'                 : ('<=', 2)
    ,'GT'                  : ('>', 2)
    ,'GTE'                 : ('>=', 2)

    # TODO(spranesh): Should we make this an if-else?
    ,'TERNARY_IF'          : ('ternary-if', 3) 

    ,'PRE_INCREMENT'       : ('pre-increment', 1)
    ,'POST_INCREMENT'      : ('post-increment', 1)
    ,'PRE_DECREMENT'       : ('pre-decrement', 1)
    ,'POST_DECREMENT'      : ('post-decrement', 1)
    ,'ADDRESS_OF'          : ('addr-of', 1)
    ,'POINTER_DEREFERENCE' : ('dereference-ptr', 1)

    ,'ATTRIBUTE_INDEX'     : ('.', 2)
    ,'ARROW'               : ('->', 2)
    ,'TYPE_CAST'           : ('cast', 2)

    # An Indexing operator (dictionaries and lists)
    ,'INDEX_INTO'          : ('index-into', 2)
}


def ExpandList(li, f):
  """ Recursively expands a list li as follows:
        For element e in the list, li:
          * If e is a list, call ExpandList(li, f) recursively.
          * If e is a Node, expand it (into a list),
              by calling ExpandList(f(e), f)"""
  if type(li) is not list:
    return

  for (i, e) in enumerate(li):
    if type(e) is list:
      li[i] = ExpandList(li[i], f)
    elif isinstance(e, Node):
      li[i] = f(e)
      if type(li[i]) is list:
        li[i] = ExpandList(li[i], f)
  return li


class Node:
  """A Parse Tree Node."""
  def __init__(self):
    raise NotImplementedError("Node is an Abstract Class.")
    return

  def __repr__(self):
    return self.GetName()

  def __str__(self):
    return self.GetName()

  def GetSExp(self):
    """ This function is not to be called directly. Code for this function is
    generated."""
    raise NotImplementedError("Base Node Class!")

  def GetChildren(self):
    """ This function is not to be called directly. Code for this function is
    generated."""
    return []

  def SetParent(self, parent):
    # We want __parent to be a private member, so that it doesnt arise in the
    # dot diagrams, or the other exported formats.
    self.__parent = parent

  def GetParent(self):
    return self.__parent

  def GetName(self):
    return self.__class__.__name__

  def MakeCopy(self):
    return copy.deepcopy(self)

  def GetAttributes(self):
    """ Return the lower case attributes of the class as a 
    pair - (class-name, dictionary-of-attributes). """
    #TODO(spranesh): Any extra attributes we are missing?
    d = {}
    # d['tags'] = []
    for x in dir(self):
      if 'a' <= x[0] <= 'z':
        d[x] = getattr(self, x)
    return (self.__class__.__name__, d)

  def GetRecursiveSExp(self):
    return ExpandList(self.GetSExp(), lambda x: x.GetSExp())

  def ToStr(self):
    return S.WriteToScheme(self)

  def GetXMLAttributes(self):
    return self.GetAttributes()

  def GetJSONAttributes(self):
    return self.GetAttributes()

  def GetDotAttributes(self):
    return self.GetAttributes()


class ControlFlowStatement(Node):
  """A base class for Control Flow statements."""
  def __init__(self):
    raise NotImplementedError("Base Class ControlFlowStatement not implemented!")

class ExceptionsStatement(Node):
  """A base class for Exceptions Related statements."""
  def __init__(self):
    raise NotImplementedError("Base Class ExceptionsStatement not implemented!")


class Assert(Node):
  """The Assert statement."""
  def __init__(self, position, test_expression, message = None):
    self.position = position
    self.test_expression = test_expression
    self.message = message
    return

  def GetChildren(self):
    li = []
    li.append(self.test_expression)
    li.append(self.message)
    return li

  def GetSExp(self):
    li = []
    li.append('assert')
    li.append(self.test_expression)
    if self.message:
      li.append([':message', self.message])
    return li



class Assignment(Node):
  """An assignment `lvalue = rvalue`"""
  def __init__(self, position, lvalue, rvalue):
    self.position = position
    self.lvalue = lvalue
    self.rvalue = rvalue
    return

  def GetChildren(self):
    li = []
    li.append(self.lvalue)
    li.append(self.rvalue)
    return li

  def GetSExp(self):
    li = []
    li.append('assign')
    li.append(self.lvalue)
    li.append(self.rvalue)
    return li



class Break(ControlFlowStatement):
  """The Break Statement."""
  def __init__(self, position):
    self.position = position
    return

  def GetSExp(self):
    li = []
    li.append('break')
    return li



class CallFunction(Node):
  """A function call. (position, function, arguments), where the function itself is a tree (with a refer variable node)."""
  def __init__(self, position, function, arguments):
    self.position = position
    self.function = function
    self.arguments = arguments
    return

  def GetChildren(self):
    li = []
    li.append(self.function)
    li.append(self.arguments)
    return li

  def GetSExp(self):
    li = []
    li.append('apply')
    li.append(self.function)
    li.append(self.arguments)
    return li



class CaseDefault(ControlFlowStatement):
  """A case or default statement."""
  def __init__(self, position, condition = None):
    self.position = position
    self.condition = condition
    return

  def GetChildren(self):
    li = []
    li.append(self.condition)
    return li

  def GetSExp(self):
    li = []
    li.append('default-or-case')
    if self.condition:
      li.append([':condition', 'case', self.condition])
    return li



class Compound(Node):
  """A compond list of items"""
  def __init__(self, position, compound_items):
    self.position = position
    self.compound_items = compound_items
    return

  def GetChildren(self):
    return self.compound_items[:]

  def GetSExp(self):
    li = []
    li.append('compound')
    li.extend(self.compound_items)
    return li



class Comprehension(Node):
  """A list (or set, dict, ..) comprehension. Python/Haskell. Type is one of 'set' or 'list' or 'generator' or 'dict'"""
  def __init__(self, position, expr, generators, type):
    self.position = position
    self.expr = expr
    self.generators = generators
    self.type = type
    return

  def GetChildren(self):
    li = []
    li.append(self.expr)
    li.append(self.generators)
    return li

  def GetSExp(self):
    li = []
    li.append('comprehension')
    li.append(self.type)
    li.append(self.expr)
    li.extend(self.generators)
    return li



class Constant(Node):
  """Represents A Constant."""
  def __init__(self, position, value, type = None):
    self.position = position
    self.value = value
    self.type = type
    return

  def GetSExp(self):
    li = []
    li.append('constant')
    li.append(self.value)
    if self.type:
      li.append([':type', self.type])
    return li



class ContextVariables(Node):
  """Variables in a Context: scope, globals, etc.."""
  def __init__(self, position, names, context):
    self.position = position
    self.names = names
    self.context = context
    return

  def GetSExp(self):
    li = []
    li.append(self.context)
    li.append('scope')
    li.append(self.names)
    return li



class Continue(ControlFlowStatement):
  """The Continue Statement."""
  def __init__(self, position):
    self.position = position
    return

  def GetSExp(self):
    li = []
    li.append('continue')
    return li



class DeclareFunction(Node):
  """A Function Declaration Node."""
  def __init__(self, position, name, arguments, return_type = None, storage = None, quals = None):
    self.position = position
    self.name = name
    self.arguments = arguments
    self.return_type = return_type
    self.storage = storage
    self.quals = quals
    return

  def GetChildren(self):
    li = []
    li.append(self.arguments)
    return li

  def GetSExp(self):
    li = []
    li.append('declare-function')
    li.append(self.name)
    li.append(self.arguments)
    if self.return_type:
      li.append([':return_type', self.return_type])
    if self.quals:
      li.append([':quals', self.quals])
    if self.storage:
      li.append([':storage', self.storage])
    return li



class DeclareSymbol(Node):
  """Declare a symbol (like an ENUM, or like a lisp symbol)."""
  def __init__(self, position, name, value = None):
    self.position = position
    self.name = name
    self.value = value
    return

  def GetChildren(self):
    li = []
    li.append(self.value)
    return li

  def GetSExp(self):
    li = []
    li.append('declare-constant')
    li.append(self.name)
    if self.value:
      li.append([':value', self.value])
    return li



class DefineClass(Node):
  """A class definition Node."""
  def __init__(self, position, name, inherits, body):
    self.position = position
    self.name = name
    self.inherits = inherits
    self.body = body
    return

  def GetChildren(self):
    li = []
    li.append(self.inherits)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('define-class')
    li.append(self.name)
    if self.inherits:
      li.append([':inherits', self.inherits])
    li.append(self.body)
    return li



class DefineFunction(Node):
  """A Function Definition Node."""
  def __init__(self, position, name, arguments, body, return_type = None, storage = None, quals = None):
    self.position = position
    self.name = name
    self.arguments = arguments
    self.body = body
    self.return_type = return_type
    self.storage = storage
    self.quals = quals
    return

  def GetChildren(self):
    li = []
    li.append(self.arguments)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('define-function')
    li.append(self.name)
    li.append(self.arguments)
    li.append(self.body)
    if self.return_type:
      li.append([':return_type', self.return_type])
    if self.quals:
      li.append([':quals', self.quals])
    if self.storage:
      li.append([':storage', self.storage])
    return li



class DefineType(Node):
  """A Type Definition."""
  def __init__(self, position, name, type):
    self.position = position
    self.name = name
    self.type = type
    return

  def GetChildren(self):
    li = []
    li.append(self.type)
    return li

  def GetSExp(self):
    li = []
    li.append('define-type')
    li.append(self.name)
    li.append(self.type)
    return li



class DefineVariable(Node):
  """A Variable Definition Node."""
  def __init__(self, position, name, init = None, type = None, quals = None, storage = None):
    self.position = position
    self.name = name
    self.init = init
    self.type = type
    self.quals = quals
    self.storage = storage
    return

  def GetSExp(self):
    li = []
    li.append('define-variable')
    li.append(self.name)
    if self.init:
      li.append([':init', self.init])
    if self.type:
      li.append([':type', self.type])
    if self.quals:
      li.append([':quals', self.quals])
    if self.storage:
      li.append([':storage', self.storage])
    return li



class Delete(Node):
  """The delete statement."""
  def __init__(self, position, targets):
    self.position = position
    self.targets = targets
    return

  def GetChildren(self):
    return self.targets[:]

  def GetSExp(self):
    li = []
    li.append('delete')
    li.extend(self.targets)
    return li



class Dict(Node):
  """A dictionary."""
  def __init__(self, position, keys, values):
    self.position = position
    self.keys = keys
    self.values = values
    return

  def GetChildren(self):
    li = []
    li.append(self.keys)
    li.append(self.values)
    return li

  def GetSExp(self):
    li = []
    li.append('dict')
    li.append(self.keys)
    li.append(self.values)
    return li



class Enumerator(Node):
  """An Enumerator."""
  def __init__(self, position, name, values):
    self.position = position
    self.name = name
    self.values = values
    return

  def GetChildren(self):
    return self.values[:]

  def GetSExp(self):
    li = []
    li.append('define-enumerator')
    li.append(self.name)
    li.append(self.values)
    return li



class ExceptionHandler(ExceptionsStatement):
  """An exception handler block"""
  def __init__(self, position, body, name = None, type = None):
    self.position = position
    self.body = body
    self.name = name
    self.type = type
    return

  def GetChildren(self):
    li = []
    li.append(self.name)
    li.append(self.type)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('exception-handler')
    if self.name:
      li.append([':name', self.name])
    if self.type:
      li.append([':type', self.type])
    li.append(self.body)
    return li



class Exec(Node):
  """The exec statement."""
  def __init__(self, position, body, globals = None, locals = None):
    self.position = position
    self.body = body
    self.globals = globals
    self.locals = locals
    return

  def GetSExp(self):
    li = []
    li.append('exec')
    li.append(self.body)
    if self.globals:
      li.append([':globals', self.globals])
    if self.locals:
      li.append([':locals', self.locals])
    return li



class Expression(Node):
  """An expression Node."""
  def __init__(self, position, operator, children):
    self.position = position
    self.operator = operator
    self.children = children
    return

  def GetChildren(self):
    return self.children[:]

  def GetSExp(self):
    li = []
    li.append(ALLOWED_OPERATORS[self.operator][0])
    li.extend(self.children)
    return li



class Finally(ExceptionsStatement):
  """Final part of an exception try-catch."""
  def __init__(self, position, body, final_body):
    self.position = position
    self.body = body
    self.final_body = final_body
    return

  def GetChildren(self):
    li = []
    li.append(self.body)
    li.append(self.final_body)
    return li

  def GetSExp(self):
    li = []
    li.append('finally')
    if self.body:
      li.append([':body', self.body])
    if self.final_body:
      li.append([':final_body', self.final_body])
    return li



class For(ControlFlowStatement):
  """A For Loop."""
  def __init__(self, position, init, condition, step, body):
    self.position = position
    self.init = init
    self.condition = condition
    self.step = step
    self.body = body
    return

  def GetChildren(self):
    li = []
    li.append(self.init)
    li.append(self.condition)
    li.append(self.step)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('for')
    li.append([self.init, self.condition, self.step])
    li.append(self.body)
    return li



class ForEach(ControlFlowStatement):
  """The For Each statement."""
  def __init__(self, position, target, iter_expression, body):
    self.position = position
    self.target = target
    self.iter_expression = iter_expression
    self.body = body
    return

  def GetChildren(self):
    li = []
    li.append(self.target)
    li.append(self.iter_expression)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('for-each')
    li.append(self.target)
    li.append(self.iter_expression)
    li.append(self.body)
    return li



class FunctionArguments(Node):
  """Function Arguments."""
  def __init__(self, position, arguments, var_arguments = None, kwd_arguments = None):
    self.position = position
    self.arguments = arguments
    self.var_arguments = var_arguments
    self.kwd_arguments = kwd_arguments
    return

  def GetChildren(self):
    li = []
    li.append(self.arguments)
    li.append(self.var_arguments)
    li.append(self.kwd_arguments)
    return li

  def GetSExp(self):
    li = []
    li.extend(self.arguments)
    if self.var_arguments:
      li.append([':var_arguments', self.var_arguments])
    if self.kwd_arguments:
      li.append([':kwd_arguments', self.kwd_arguments])
    return li



class FunctionDecorator(Node):
  """Function Decorator"""
  def __init__(self, position, decorator, function):
    self.position = position
    self.decorator = decorator
    self.function = function
    return

  def GetChildren(self):
    li = []
    li.append(self.decorator)
    li.append(self.function)
    return li

  def GetSExp(self):
    li = []
    li.append('function-decorator')
    li.append(self.decorator)
    li.append(self.function)
    return li



class Generator(Node):
  """The generator of a comprehension `for x in .. if ..` Python/Haskell. (A helper node for comprehension). Condition is a single condition"""
  def __init__(self, position, target, generator, condition = None):
    self.position = position
    self.target = target
    self.generator = generator
    self.condition = condition
    return

  def GetChildren(self):
    li = []
    li.append(self.target)
    li.append(self.generator)
    li.append(self.condition)
    return li

  def GetSExp(self):
    li = []
    li.append(self.target)
    li.append(self.generator)
    if self.condition:
      li.append([':condition', self.condition])
    return li



class Goto(ControlFlowStatement):
  """The Goto construct. Considered Harmful, yea?"""
  def __init__(self, position, location):
    self.position = position
    self.location = location
    return

  def GetSExp(self):
    li = []
    li.append('goto')
    li.append(self.location)
    return li



class IfElse(ControlFlowStatement):
  """An If Else Node."""
  def __init__(self, position, condition, if_true, if_false = None):
    self.position = position
    self.condition = condition
    self.if_true = if_true
    self.if_false = if_false
    return

  def GetChildren(self):
    li = []
    li.append(self.condition)
    li.append(self.if_true)
    li.append(self.if_false)
    return li

  def GetSExp(self):
    li = []
    li.append('if')
    li.append(self.condition)
    li.append(self.if_true)
    li.append(self.if_false)
    return li



class Import(Node):
  """The import construct. import module_name as as_name"""
  def __init__(self, position, import_aliases):
    self.position = position
    self.import_aliases = import_aliases
    return

  def GetChildren(self):
    return self.import_aliases[:]

  def GetSExp(self):
    li = []
    li.append('import')
    li.append(self.import_aliases)
    return li



class ImportFrom(Import):
  """The import from construct. from module_name import x,y,z"""
  def __init__(self, position, module, import_aliases):
    self.position = position
    self.module = module
    self.import_aliases = import_aliases
    return

  def GetChildren(self):
    return self.import_aliases[:]

  def GetSExp(self):
    li = []
    li.append('from')
    li.append(self.module)
    li.append('import')
    li.append(self.import_aliases)
    return li



class Lambda(Node):
  """A Lambda Function"""
  def __init__(self, position, arguments, value):
    self.position = position
    self.arguments = arguments
    self.value = value
    return

  def GetChildren(self):
    li = []
    li.append(self.arguments)
    li.append(self.value)
    return li

  def GetSExp(self):
    li = []
    li.append('lambda')
    li.append(self.arguments)
    li.append(self.value)
    return li



class Let(Node):
  """A Let binding."""
  def __init__(self, position, defvars, body):
    self.position = position
    self.defvars = defvars
    self.body = body
    return

  def GetChildren(self):
    li = []
    li.append(self.defvars)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('with')
    li.append(self.defvars)
    li.append(self.body)
    return li



class List(Node):
  """A List."""
  def __init__(self, position, values):
    self.position = position
    self.values = values
    return

  def GetChildren(self):
    return self.values[:]

  def GetSExp(self):
    return self.values[:]



class Module(Node):
  """Represents a file or module."""
  def __init__(self, position, filename, children):
    self.position = position
    self.filename = filename
    self.children = children
    return

  def GetChildren(self):
    return self.children[:]

  def GetSExp(self):
    li = []
    li.append('define-module')
    li.append(self.filename)
    li.append(self.children)
    return li



class ModuleAlias(Node):
  """Import Aliases."""
  def __init__(self, position, name, asmodule = None):
    self.position = position
    self.name = name
    self.asmodule = asmodule
    return

  def GetSExp(self):
    li = []
    li.append('module-alias')
    li.append(self.name)
    if self.asmodule:
      li.append([':asmodule', self.asmodule])
    return li



class Pass(ControlFlowStatement):
  """The Pass Statement."""
  def __init__(self, position):
    self.position = position
    return

  def GetSExp(self):
    li = []
    li.append('pass')
    return li



class Print(Node):
  """The Print statement."""
  def __init__(self, position, values, stream = None):
    self.position = position
    self.values = values
    self.stream = stream
    return

  def GetChildren(self):
    li = []
    li.append(self.values)
    li.append(self.stream)
    return li

  def GetSExp(self):
    li = []
    li.append('print')
    li.append(self.values)
    if self.stream:
      li.append([':stream', self.stream])
    return li



class Raise(ExceptionsStatement):
  """Raise an Exception."""
  def __init__(self, position, exception_type):
    self.position = position
    self.exception_type = exception_type
    return

  def GetChildren(self):
    li = []
    li.append(self.exception_type)
    return li

  def GetSExp(self):
    li = []
    li.append('raise-exception')
    li.append(self.exception_type)
    return li



class ReferVariable(Node):
  """A variable reference."""
  def __init__(self, position, name):
    self.position = position
    self.name = name
    return

  def GetSExp(self):
    return self.name[:]



class Return(Node):
  """Represents a Return Statement."""
  def __init__(self, position, return_expression):
    self.position = position
    self.return_expression = return_expression
    return

  def GetChildren(self):
    li = []
    li.append(self.return_expression)
    return li

  def GetSExp(self):
    li = []
    li.append('return')
    li.append(self.return_expression)
    return li



class Slice(Node):
  """A slice node."""
  def __init__(self, position, lower = None, upper = None, step = None):
    self.position = position
    self.lower = lower
    self.upper = upper
    self.step = step
    return

  def GetChildren(self):
    li = []
    li.append(self.lower)
    li.append(self.upper)
    li.append(self.step)
    return li

  def GetSExp(self):
    li = []
    li.append('slice')
    if self.lower:
      li.append([':lower', self.lower])
    if self.upper:
      li.append([':upper', self.upper])
    if self.step:
      li.append([':step', self.step])
    return li



class SourceLabel(Node):
  """A label in the source. Like the Goto labels."""
  def __init__(self, position, name, statements):
    self.position = position
    self.name = name
    self.statements = statements
    return

  def GetChildren(self):
    li = []
    li.append(self.statements)
    return li

  def GetSExp(self):
    li = []
    li.append('label')
    li.append(self.name)
    li.append(self.statements)
    return li



class Structure(Node):
  """A structure type"""
  def __init__(self, position, name, members, storage = None, quals = None):
    self.position = position
    self.name = name
    self.members = members
    self.storage = storage
    self.quals = quals
    return

  def GetChildren(self):
    return self.members[:]

  def GetSExp(self):
    li = []
    li.append('define-structure')
    li.append(self.name)
    li.append(self.members)
    if self.storage:
      li.append([':storage', self.storage])
    if self.quals:
      li.append([':quals', self.quals])
    return li



class Switch(ControlFlowStatement):
  """A Swith Case Statement"""
  def __init__(self, position, switch_on, body):
    self.position = position
    self.switch_on = switch_on
    self.body = body
    return

  def GetChildren(self):
    li = []
    li.append(self.switch_on)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('switch')
    li.append(self.switch_on)
    li.append(self.body)
    return li



class TryCatch(ExceptionsStatement):
  """A Try-Catch block."""
  def __init__(self, position, body, exception_handlers, orelse):
    self.position = position
    self.body = body
    self.exception_handlers = exception_handlers
    self.orelse = orelse
    return

  def GetChildren(self):
    li = []
    li.append(self.body)
    li.append(self.exception_handlers)
    li.append(self.orelse)
    return li

  def GetSExp(self):
    li = []
    li.append('catch-exception')
    li.append(self.body)
    if self.exception_handlers:
      li.append([':exception_handlers', self.exception_handlers])
    if self.orelse:
      li.append([':orelse', self.orelse])
    return li



class Tuple(Node):
  """A Tuple."""
  def __init__(self, position, members):
    self.position = position
    self.members = members
    return

  def GetChildren(self):
    return self.members[:]

  def GetSExp(self):
    return self.members[:]



class Union(Node):
  """A union type"""
  def __init__(self, position, name, members):
    self.position = position
    self.name = name
    self.members = members
    return

  def GetChildren(self):
    return self.members[:]

  def GetSExp(self):
    li = []
    li.append('define-union')
    li.append(self.name)
    li.append(self.members)
    return li



class While(ControlFlowStatement):
  """Represents a While Loop."""
  def __init__(self, position, condition, body, do_while = None):
    self.position = position
    self.condition = condition
    self.body = body
    self.do_while = do_while
    return

  def GetChildren(self):
    li = []
    li.append(self.condition)
    li.append(self.body)
    return li

  def GetSExp(self):
    li = []
    li.append('while')
    if self.do_while:
      li.append([':do_while', 'true'])
    li.append(self.condition)
    li.append(self.body)
    return li



class Yield(Node):
  """Yield Statement"""
  def __init__(self, position, yield_expression):
    self.position = position
    self.yield_expression = yield_expression
    return

  def GetChildren(self):
    li = []
    li.append(self.yield_expression)
    return li

  def GetSExp(self):
    li = []
    li.append('yield')
    li.append(self.yield_expression)
    return li


