""" Type Classes.
    
    Used to structure the Type Heirarchy.
    
    This file is AUTO GENERATED from
      _types_cfg.yaml using _ast_gen.py
    The header is stored in _types_header.py
"""

import node

class Type(node.Node):
  """ The Base Type class."""
  pass



class Array(Type):
  """Represents an array type."""
  def __init__(self, array_type):
    self.array_type = array_type
    return

  def GetChildren(self):
    li = []
    li.append(self.array_type)
    return li

  def GetSExp(self):
    li = []
    li.append('array-of')
    li.append(self.array_type)
    return li



class BaseType(Type):
  """Represents a base type (stored as a string)."""
  def __init__(self, base_type):
    self.base_type = base_type
    return

  def GetSExp(self):
    li = []
    li.append('base-type')
    li.append(self.base_type)
    return li



class Pointer(Type):
  """Represents a Pointer-to type."""
  def __init__(self, ptr_type):
    self.ptr_type = ptr_type
    return

  def GetChildren(self):
    li = []
    li.append(self.ptr_type)
    return li

  def GetSExp(self):
    li = []
    li.append('pointer-to')
    li.append(self.ptr_type)
    return li



class StructureType(Type):
  """Represents a Structure type."""
  def __init__(self, structure_type):
    self.structure_type = structure_type
    return

  def GetChildren(self):
    li = []
    li.append(self.structure_type)
    return li

  def GetSExp(self):
    li = []
    li.append('structure-to')
    li.append(self.structure_type)
    return li


