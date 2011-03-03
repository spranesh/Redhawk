""" Type Heirarchy. """
import node
import util

class Type(node.Node):
  """ Type Class."""
  pass


class BaseType(Type):
  def __init__(self, s):
    assert(type(s) is str)
    self.type = s
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level=0):
    return ["base-type", self.type]


class Array(Type):
  def __init__(self, t):
    assert(isinstance(t, Type))
    self.type = t
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return ["array-of", self.type]


class Pointer(Type):
  def __init__(self, t):
    assert(isinstance(t, Type))
    self.type = t
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return ["pointer-to", self.type]


class Structure(Type):
  def __init__(self, types):
    for i in types:
      assert(isinstance(i, Type))
    self.types = types
    return

  @util.ConvertToStringWithIndent
  def ToStr(self, indent_level = 0):
    return ["structure-of"].extend(self.types)
