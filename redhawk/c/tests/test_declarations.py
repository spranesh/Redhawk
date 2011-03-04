#!/usr/bin/env python

""" Test various kinds of declarations.
    Declarations are present in the declarations.c file.

    Note that these tests only check that conversion works, and not that the
    resultant tree is actually correct (yet)."""

import test_utils

def TestDeclaration1():
  """ Test `int a` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[0])

def TestDeclaration2():
  """ Test `int *b` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[1])

def TestDeclaration3():
  """ Test `char *c` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[2])

def TestDeclaration4():
  """ Test `void *d = NULL` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[3])

def TestDeclaration5():
  """ Test `int e = 0` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[4])

def TestDeclaration6():
  """ Test `static const char * p;` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[5])

def TestDeclaration7():
  """ Test `int foo(int a, int b)` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[6])

def TestDeclaration8():
  """ Test `int foo(int, int)` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[7])

def TestDeclaration9():
  """ Test `static foo (int, int)` """
  t = test_utils.SetUp("declarations.c")
  return test_utils.ConvertTree(t.children()[8])

