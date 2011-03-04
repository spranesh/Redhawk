""" The Node Class. """

import util

import copy

class Node:
  """ Signifies a node in the parse tree."""
  def __init__(self):
    raise NotImplementedError("Node is an Abstract Class.")
    return

  def __repr__(self):
    return self.ToStr()

  def __str__(self):
    return self.ToStr()

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
  def __init__(self, position, name, init = None, type = None):
    self.position = position
    self.type = type
    self.name = name
    self.init = init

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    li = ["define-variable", self.name]
    if self.init:
      li.append([":init", self.init])
    if self.type:
      li.append([":type", self.type])
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
    return

  # This has been separated to make avoid duplicating work in DefineFunction
  def GetNodeContentsAsList(self):
    li = [self.name]
    if len(self.arguments) is not 0:
      li.append(["arguments"] + self.arguments)
    if self.return_type:
      li.append([":return-type", self.return_type])
    return li

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    li = self.GetNodeContentsAsList()
    li.insert(0, "declare-function")
    return li


# Is inheriting from DeclareFunction a good thing to be doing?
class DefineFunction(DeclareFunction):
  def __init__(self, position, name, arguments, body, return_type):
    DeclareFunction.__init__(self, position, name, arguments, return_type)
    self.body = body
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
