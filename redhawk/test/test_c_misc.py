#!/usr/bin/env python

""" Miscellaneous Node Tests for the tree conversion. """

from __future__ import absolute_import
from . import c_test_utils as CT

def TestReturnConstant(): 
  """ Test `return 0`"""
  t = CT.SetUp("prog001.c")
  main = t.children()[0]
  return_node = main.body.block_items[0]
  return CT.ConvertTree(return_node)

def TestFileAST1():
  """ Test FileAST """
  t = CT.SetUp("simple_declaration.c")
  return CT.ConvertTree(t, "simple_declaration.c")

def TestFunctionDefinition1():
  """ Test Function Definition."""
  t = CT.SetUp("prog001.c")
  return CT.ConvertTree(t.children()[0])

