""" Node Classes.

    This file is AUTO GENERATED from
      node_cfg.yaml using _ast_gen.py
    The header is stored in node_header.py
"""

import writers.scheme_writer as S

import copy
import pprint

# A dictionary of allowed operators, and their arity.
ALLOWED_OPERATORS = {
     'UNARY_MINUS'         : ('-', 1)
    ,'UNARY_PLUS'          : ('+', 1)
    ,'SIZE_OR_LEN'         : ('size-or-len-of', 1)

    ,'MULTIPLY'            : ('*', 2)
    ,'ADD'                 : ('+', 2)
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

    ,'BOOLEAN_AND'         :('and', 2)
    ,'BOOLEAN_OR'          : ('or', 2)
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

  def GetName(self):
    return self.__class__.__name__

  def MakeCopy(self):
    return copy.deepcopy(self)

  def GetChildren(self):
    return []

  def ToStr(self):
    return S.WriteToScheme(self)

  def GetSExp(self):
    raise NotImplementedError("Base Node Class!")

  def GetRecursiveSExp(self):
    return ExpandList(self.GetSExp(), lambda x: x.GetSExp())

  def GetAttributes(self):
    """ Return the lower case attributes of the class as a 
    pair - (class-name, dictionary-of-attributes). """
    #TODO(spranesh): Any extra attributes we are missing?
    d = {}
    d['tags'] = []
    for x in dir(self):
      if 'a' <= x[0] <= 'z':
        d[x] = getattr(self, x)
    return (self.__class__.__name__, d)

  def GetXMLAttributes(self):
    return self.GetAttributes()

  def GetJSONAttributes(self):
    return self.GetAttributes()

  def GetDotAttributes(self):
    return self.GetAttributes()



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
    li.append(self.function)
    li.extend(self.arguments)
    return li



class CaseDefault(Node):
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
    return self.compound_items

  def GetSExp(self):
    li = []
    li.append('compound')
    li.extend(self.compound_items)
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
      li.append([':type', ':type', self.type])
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



class Expression(Node):
  """An expression Node."""
  def __init__(self, position, operator, children):
    self.position = position
    self.operator = operator
    self.children = children
    return

  def GetChildren(self):
    return self.children

  def GetSExp(self):
    li = []
    li.append(ALLOWED_OPERATORS[self.operator][0])
    li.extend(self.children)
    return li



class For(Node):
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



class IfElse(Node):
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



class List(Node):
  """A List."""
  def __init__(self, position, values):
    self.position = position
    self.values = values
    return

  def GetChildren(self):
    return self.values

  def GetSExp(self):
    return self.values



class Module(Node):
  """Represents a file or module."""
  def __init__(self, filename, children):
    self.filename = filename
    self.children = children
    return

  def GetChildren(self):
    return self.children

  def GetSExp(self):
    li = []
    li.append('define-module')
    li.append(self.filename)
    li.append(self.children)
    return li

  def GetXMLAttributes(self):
    d = {}
    d['tags'] = []
    d['tags'].append('define-module')
    d[filename] = self.filename
    return (self.__class__.__name__, d)



class ReferVariable(Node):
  """A variable reference."""
  def __init__(self, position, name):
    self.position = position
    self.name = name
    return

  def GetSExp(self):
    return self.name



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
    return self.members

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



class Switch(Node):
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



class While(Node):
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


