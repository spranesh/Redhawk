""" Node Classes.

    This file is AUTO GENERATED from
      node_cfg.yaml using _ast_gen.py
    The header is stored in node_header.py
"""

from __future__ import absolute_import
from .writers import scheme_writer as S
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

  def GetFlattenedChildren(self):
    """ Get a list of flattened children. This method caches the flattened
    children before returning it, to prevent repeated calls to
    U.Flatten(..)."""
    if not hasattr(self, 'flattened_children_cache'):
      flattened_children = U.Flatten(self.GetChildren())
      self.flattened_children_cache = flattened_children
    return self.flattened_children_cache

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

