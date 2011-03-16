""" The Node Class. """

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


class Node:
  """A Parse Tree Node."""
  def __init__(self):
    raise NotImplementedError("Node is an Abstract Class.")
    return

  def __repr__(self):
    return self.ToStr()

  def __str__(self):
    return self.ToStr()

  def MakeCopy(self):
    return copy.deepcopy(self)

  def GetChildren(self):
    raise NotImplementedError("Base Node Class!")

  def ToStr():
    return pprint.pformat(self.GetSExp())

  def GetSExp(self):
    raise NotImplementedError("Base Node Class!")

  def GetAttributes(self):
    """ Return the attributes of the class as a 
    pair - (class-name, dictionary-of-attributes). """
    d = {}
    d['tags'] = []
    for x in dir(self):
      if 'a' <= x[0] <= 'z':
        d[x] = getattr(self, x)
    return (self.__name__.__class__, d)

  def GetXMLAttributes(self):
    return self.GetAttributes()

  def GetJSONAttributes(self):
    return self.GetAttributes()

  def GetDotAttributes(self):
    return self.GetAttributes()

