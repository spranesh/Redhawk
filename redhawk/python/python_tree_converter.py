#!/usr/bin/env python
import redhawk.common.node as N
import redhawk.common.node_position as NP
import redhawk.common.tree_converter as tree_converter
# import redhawk.common.types as T

# Map Python AST operators into the L-AST operators
# Add | Sub | Mult | Div | Mod | Pow | LShift 
#                  | RShift | BitOr | BitXor | BitAnd | FloorDiv
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
     # ,'<'       : 'LT'
     # ,'>'       : 'GT'
     # ,'<='      : 'LTE'
     # ,'>='      : 'GTE'
     # ,'=='      : 'EQ'
     # ,'!='      : 'NOT_EQ'
     # ,'&&'      : 'BOOLEAN_AND'
     # ,'||'      : 'BOOLEAN_OR'

     # ,'.'       : 'ATTRIBUTE_INDEX'
     # ,'->'      : 'ARROW' # TODO(spranesh): Bad Name?
}

class TransformCoord:
  """ A class to help transform coordinates from the python ast to the L-AST.
  This has been made a class, because it has state."""
  def __init__(self, filename):
    self.filename = filename
    return

  # Get Coord
  def GC(self, c):
    NP.NodePosition(self.filename, c.lineno, c.col_offset)

def GetClassName(x):
  return x.__class__.__name__

class PythonTreeConverter(tree_converter.TreeConverter):
  def __init__(self, filename=None):
    tree_converter.TreeConverter.__init__(self, filename)
    self.gc = TransformCoord(filename)
    return

  def ConvertExpr(self, tree):
    return self.ConvertTree(tree.value)

  def ConvertNum(self, tree):
    #TODO(spranesh): Should the value be really str-ed?
    return N.Constant(self.gc.GC(tree),
        value = str(tree.n),
        type = None)

  def ConvertBinop(self, tree):
    return N.Expression(position = self.gc.GC(tree),
        operator = BINARY_OPERATOR_CONVERSIONS[GetClassName(tree.op)],
        children = map(self.ConvertTree, [tree.left, tree.right]))

  def ConvertName(self, tree):
    return N.ReferVariable(self.gc.GC(tree),
        name = tree.id)

