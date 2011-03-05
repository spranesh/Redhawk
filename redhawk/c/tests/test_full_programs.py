#!/usr/bin/env python

""" Tests converstion of full programs. """

import test_utils

def TestProgram1():
  """ Test prog001.c (Function to return 0)"""
  t = test_utils.SetUp("prog001.c")
  return test_utils.ConvertTree(t)

def TestProgram2():
  """ Test prog002.c (Static function to return 0)"""
  t = test_utils.SetUp("prog002.c")
  return test_utils.ConvertTree(t)

def TestProgram3():
  """ Test prog003.c (An expression)"""
  t = test_utils.SetUp("prog003.c")
  return test_utils.ConvertTree(t)

def TestProgram4():
  """ Test prog004.c (Variable Declaration)"""
  t = test_utils.SetUp("prog004.c")
  return test_utils.ConvertTree(t)

def TestProgram5():
  """ Test prog005.c (Pointer Declaration)"""
  t = test_utils.SetUp("prog005.c")
  return test_utils.ConvertTree(t)

def TestProgram6():
  """ Test prog006.c (Point to array of chars)"""
  t = test_utils.SetUp("prog006.c")
  return test_utils.ConvertTree(t)

def TestProgram7():
  """ Test prog007.c (Assignment Statements)"""
  t = test_utils.SetUp("prog007.c")
  return test_utils.ConvertTree(t)

def TestProgram8():
  """ Test prog008.c (function call) """
  t = test_utils.SetUp("prog008.c")
  return test_utils.ConvertTree(t)
