#!/usr/bin/env python

""" Test Expressions """

import test_utils
import nose.tools

ConvertTree = test_utils.ConvertTree

def SetUp(filename):
  t = test_utils.SetUp(filename)
  test_descriptions = open("%s/%s"%(test_utils.RELATIVE_TEST_PATH, filename)).readlines()

  return (t, test_descriptions)


def TestExpressions():
  filename = "expressions.py"
  
  (t, test_descriptions) = SetUp(filename)
  for i in range(len(t.body)):
    description = test_descriptions[i]
    ConvertTree.description = "Test [%s]:`%s`"%(filename, description.strip())
    yield ConvertTree, t.body[i]



def TestStatements():
  filename = "statements.py"

  (t, test_descriptions) = SetUp(filename)
  for i in range(len(t.body)):
    description = test_descriptions[i]
    ConvertTree.description = "Test [%s]:`%s`"%(filename, description.strip())
    yield ConvertTree, t.body[i]
