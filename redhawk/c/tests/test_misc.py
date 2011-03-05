#!/usr/bin/env python

""" Miscellaneous Node Tests for the tree conversion. """

import test_utils

def TestReturnConstant(): 
  """ Test `return 0`"""
  t = test_utils.SetUp("prog001.c")
  main = t.children()[0]
  return_node = main.body.block_items[0]
  return test_utils.ConvertTree(return_node)

def TestFileAST1():
  """ Test FileAST """
  t = test_utils.SetUp("simple_declaration.c")
  return test_utils.ConvertTree(t, "simple_declaration.c")

def TestFunctionDefinition1():
  """ Test Function Definition."""
  t = test_utils.SetUp("prog001.c")
  return test_utils.ConvertTree(t.children()[0])

