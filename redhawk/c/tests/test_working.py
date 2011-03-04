#!/usr/bin/env python

""" Tests whether all the transformations are in place to convert the
programs. """

import test_utils

def TestReturnConstant(): 
  """ Test `return 0`"""
  t = test_utils.SetUp("prog001.c")
  main = t.children()[0]
  return_node = main.body.block_items[0]
  return test_utils.ConvertTree(return_node)

def TestDeclaration1():
  """ Test `int a` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[0])

def TestDeclaration2():
  """ Test `int *b` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[1])

def TestDeclaration3():
  """ Test `char *c` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[2])

def TestDeclaration4():
  """ Test `void *d = NULL` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[3])

def TestDeclaration5():
  """ Test `int e = 0` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[4])

def TestDeclaration6():
  """ Test `int foo(int a, int b)` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[5])

def TestDeclaration7():
  """ Test `int foo(int, int)` """
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t.children()[6])


# def Test002(): ConvertProgram("prog002.c")
# def Test003(): ConvertProgram("prog003.c")
# def Test004(): ConvertProgram("prog004.c")

