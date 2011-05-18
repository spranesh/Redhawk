#!/usr/bin/env python

""" Test xpath query functionality."""

import redhawk.common.selector as S
from sample_last import module_tree
import redhawk.common.xpath as X


""" The sample tree that we will test the selectors on:
(module
  (define-function Factorial 
    ((define-variable n))
    ((if 
      (eq n 
        (constant 0))
      ((return 
        (constant 1)))
      ((return 
        (* n 
          (apply Factorial 
            ((- n 
              (constant 1)))))))))))
"""

def Query(query):
  parsed_query = X.ParseXPath(query)
  return set(X.ApplyParsedXPathQuery([module_tree], parsed_query))

def TestEmptySelector():
  """ Test the Empty Selector (Should return all nodes)."""
  assert(len(Query('**')) == 19) # Number of nodes in the tree.
  return

def TestSelector():
  """ Test Basic Node queries - function, attributes, node_type"""
  l0 = list(Query('DefineFunction'))
  l1 = list(Query('**/DefineFunction'))
  l2 = list(Query('**/@[value="0"]'))
  l3 = list(Query('**/@{n.value == "0"}'))
  l4 = list(Query('**/@{n.value == "1"}'))

  print l0
  print l1
  print l2
  print l3
  print l4
  assert(l0 == l1)
  assert(l2 == l3)

  assert(len(l1) == 1 and len(l2) == 1 and len(l4) == 2)
  assert(l2 == l3)

  r1, r2, r3, r4 = l1[0], l2[0], l4[0], l4[1]

  assert(r1.name == 'Factorial')
  assert(r2.GetName() == 'Constant')
  assert(r3.GetName() == 'Constant')
  assert(r4.GetName() == 'Constant')
  return

def TestPositionSelector():
  l0 = list(Query('**/DefineFunction/[0]'))
  l1 = list(Query('**/DefineFunction/[1]'))
  l2 = list(Query('**/DefineFunction/[2]'))

  assert(len(l0) == len(l1) == 1)
  assert(l0[0].GetName() == 'FunctionArguments')
  assert(l1[0].GetName() == 'IfElse')
  assert(l2 == [])

  l0 = list(Query('**/DefineFunction/FunctionArguments/[0, 0]'))
  assert(len(l0) == 1)
  assert(l0[0].GetName() == 'DefineVariable')

  # We should be getting a return which is a child of the else clause
  r = list(Query('**/IfElse/Return[2]'))
  q = list(Query('**/IfElse/Return[2, 0]'))
  assert(len(r) == 1)
  assert(r == q)
  assert(r[0].GetChildren()[0].GetName() == 'Expression')
  return

def TestDot():
  """ Test Dot """
  assert(list(Query("./././././."))[0] == module_tree)
  return

def TestDotDot():
  """ Test Dot Dot """
  assert(list(Query("*/.."))[0] == module_tree)
  assert(list(Query("*/*/*/../../.."))[0] == module_tree)
  assert(list(Query("..")) == [])
  assert(list(Query("*/../..")) == [])
  return

def TestStar():
  """ Test Star """
  p = list(Query('*/.'))
  q = list(Query('*/*/.'))
  assert(len(p) == 1)
  assert(len(q) == 2)
  assert(p[0].GetName() == 'DefineFunction')
  assert(q[0] != q[1])
  assert(q[0].GetName() in ['FunctionArguments', 'IfElse'])
  assert(q[1].GetName() in ['FunctionArguments', 'IfElse'])
  return

def TestQuery1():
  """ Test Star Star """
  r = list(Query('CallFunction'))
  assert(r == [])
  r = list(Query('**/CallFunction'))
  assert(len(r) == 1)
  return

def TestCombinations():
  """ Test Combinations """
  r = list(Query('**/Return/**/Expression'))
  assert(len(r) == 2)
  assert(r[0].GetName() == "Expression")
  assert(r[1].GetName() == "Expression")
  r = list(Query('**/Return/**/CallFunction'))
  x = list(Query('**/CallFunction'))
  assert(x[0] == r[0])
  return

def TestChildNodeQuery():
  """ Test Child node query """
  l = list(Query("**/Return/(CallFunction)/../.."))
  print l
  
def TestIfElse():
  """ Test that sure **, Path, and numbering give same result."""
  l1 = list(Query("**/IfElse"))
  l2 = list(Query("DefineFunction/IfElse"))
  l3 = list(Query("DefineFunction/[1]"))
  print l1, l2, l3
  assert(l1 == l2 == l3)

def TestStarStarCurrentLevel():
  """ Test that ** can be used for the current level."""
  l1 = list(Query("**/FunctionArguments"))
  l2 = list(Query("**/DefineFunction/**/FunctionArguments"))
  assert(len(l1) == 2)
  l1.sort()
  l2.sort()
  assert(l1 == l2)
  return

def TestLastLevel():
  """ Test Things at a leaf node."""
  l1 = list(Query("**/Constant"))
  l2 = list(Query("**/Constant/../Constant"))
  l3 = list(Query("**/Constant/../Constant"))
  l1.sort()
  l2.sort()
  l3.sort()
  assert(l1 == l2 == l3)
  return


def TestMultipleAttributes():
  """ Test Mutiple Attributes."""
  l = list(Query('**/@[value="0"]@[value="0"]'))
  assert(len(l) == 1)
  assert(l[0].GetName() == "Constant")

def TestEqualityOfChildNode():
  """ Test equality of [a] and a/.."""
  l1 = list(Query('**/(Constant@[value="0"])'))
  l2 = list(Query('**/Constant@[value="0"]/..'))
  assert(len(l1) == len(l2) == 1)
  assert(l1 == l2)
  l1 = list(Query('**/(Constant@[value="1"])'))
  l2 = list(Query('**/Constant@[value="1"]/..'))
  l1.sort()
  l2.sort()
  assert(l1 == l2)

