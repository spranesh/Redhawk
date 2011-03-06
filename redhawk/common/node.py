""" The Node Class. """

import util

import copy

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
}



class Node:
  """ Signifies a node in the parse tree."""
  def __init__(self):
    raise NotImplementedError("Node is an Abstract Class.")
    return

  def __repr__(self):
    return self.ToStr()

  def __str__(self):
    return self.ToStr()

  def MakeCopy(self):
    return copy.deepcopy(self)

  def ToStr(self):
    """ Should return a list of lines, which will be indented by the
    whitespace argument using a function decorator."""
    raise NotImplementedError("Not implemented for the Base Node Class.")

class Module(Node):
  def __init__(self, position, children):
    self.position = position
    self.children = children
    self.filename = position.GetFile()

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    return ["define-module", self.filename, self.children]

class Constant(Node):
  def __init__(self, position, value, type=None):
    self.value = value
    self.type = type
    self.position = position
    return
  
  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    return ["constant", str(self.value), [":type", self.type]]


class Return(Node):
  def __init__(self, position, return_expression):
    self.position = position
    self.return_expression = return_expression
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    return ["return", self.return_expression]


class DefineVariable(Node):
  def __init__(self, position, name, init = None, type = None, quals = None,
      storage = None):
    self.position = position
    self.type = type
    self.name = name
    self.init = init
    self.quals = quals
    self.storage = storage

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    li = ["define-variable", self.name]
    if self.init:
      li.append([":init", self.init])
    if self.type:
      li.append([":type", self.type])
    if self.quals:
      li.append([":quals", self.quals])
    if self.storage:
      li.append([":storage", self.storage])
    return li


class DeclareFunction(Node):
  def __init__(self, position, name, arguments, return_type):
    """ Name is a string, arguments a list of variable declarations, and
    return_type a type object. """
    assert(type(arguments) is list)
    self.position = position
    self.name = name
    self.arguments = arguments
    self.return_type = return_type
    self.storage = None
    self.quals = None
    return

  # This has been separated to make avoid duplicating work in DefineFunction
  def GetNodeContentsAsList(self):
    li = [self.name]
    if len(self.arguments) is not 0:
      li.append(["arguments"] + self.arguments)
    if self.return_type:
      li.append([":return-type", self.return_type])
    if self.storage:
      li.append([":storage", self.storage])
    if self.quals:
      li.append([":quals", self.quals])
    return li

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    li = self.GetNodeContentsAsList()
    li.insert(0, "declare-function")
    return li


# Is inheriting from DeclareFunction a good thing to be doing?
class DefineFunction(DeclareFunction):
  def __init__(self, position, name, arguments, body, return_type, 
      storage = None, quals = None):
    DeclareFunction.__init__(self, position, name, arguments, return_type)
    self.body = body
    self.storage = storage
    self.quals = quals
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    li = self.GetNodeContentsAsList()
    li.append(self.body)
    li.insert(0, "define-function")
    return li


class Compound(Node):
  def __init__(self, position, compound_items):
    self.position = position
    self.compound_items = compound_items
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return ["compound"] + self.compound_items


class Expression(Node):
  def __init__(self, position, operator, children):
    assert(operator in ALLOWED_OPERATORS)
    assert(len(children) is ALLOWED_OPERATORS[operator][1])
    self.position = position
    self.operator = operator
    self.children = children

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    operator_str = ALLOWED_OPERATORS[self.operator][0]
    return [operator_str] + self.children


class ReferVariable(Node):
  def __init__(self, position, name):
    self.position = position
    self.name = name

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return self.name


class Assignment(Node):
  def __init__(self, position, lvalue, rvalue):
    self.position = position
    self.lvalue = lvalue
    self.rvalue = rvalue
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return ["assign", self.lvalue, self.rvalue]


class CallFunction(Node):
  def __init__(self, position, function, arguments):
    # TODO(spranesh): function is currently a tree, and not just a name.
    # Is there any way to sort this out?
    # Right now, we will have to search for CallFunction, and then go down
    # till we hit a ReferVariable node
    self.position = position
    self.function = function
    self.arguments = arguments
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return [self.function] + self.arguments


class Structure(Node):
  def __init__(self, position, name, members, storage = None, quals = None):
    self.position = position
    self.name = name
    self.members = members
    self.storage = storage
    self.quals = quals
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    li = ["define-structure", self.name, self.members]
    if self.storage:
      li.append([":storage", self.storage])
    if self.quals:
      li.append([":quals", self.quals])
    return li


class IfElse(Node):
  def __init__(self, position, condition, if_true, if_false=None):
    assert(condition is not None)
    assert(if_true is not None)
    self.position = position
    self.condition = condition
    self.if_true = if_true
    self.if_false = if_false
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    li = ["if", self.condition, self.if_true]
    if self.if_false:
      li.append(self.if_false)
    return li


class For(Node):
  def __init__(self, position, init, condition, step, body):
    self.position = position
    self.init = init
    self.condition = condition
    self.step = step
    self.body = body
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    li = ["for", [self.init, self.condition, self.step]]
    if self.body:
      li.append(self.body)
    return li


class While(Node):
  def __init__(self, position, condition, body, do_while=False):
    self.position = position
    self.condition = condition
    self.body = body
    self.do_while = do_while
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    if self.do_while:
      li = ["do-while"]
    else:
      li = ["while"]
    
    li.extend([self.condition, self.body])
    return li


class Switch(Node):
  def __init__(self, position, switch_on, body):
    self.position = position
    self.switch_on = switch_on
    self.body = body
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return ["switch", self.switch_on, self.body]


class CaseDefault(Node):
  def __init__(self, position, condition=None):
    # Condition is None => default
    self.position = position
    self.condition = condition
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    if self.condition is None:
      return ["default", self.condition]
    else:
      return ["case", self.condition]

