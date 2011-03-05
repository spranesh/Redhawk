#!/usr/bin/env python

""" Tests converstion of full programs. """

import test_utils

def TestProgram1():
  """ Test prog001.c """
  t = test_utils.SetUp("prog001.c")
  return test_utils.ConvertTree(t)

def TestProgram2():
  """ Test prog002.c """
  t = test_utils.SetUp("prog002.c")
  return test_utils.ConvertTree(t)

def TestProgram3():
  """ Test prog003.c """
  t = test_utils.SetUp("prog003.c")
  return test_utils.ConvertTree(t)

def TestProgram4():
  """ Test prog004.c """
  t = test_utils.SetUp("prog004.c")
  return test_utils.ConvertTree(t)

def TestProgram5():
  """ Test prog005.c """
  t = test_utils.SetUp("prog005.c")
  return test_utils.ConvertTree(t)

def TestProgram6():
  """ Test prog006.c """
  t = test_utils.SetUp("prog006.c")
  return test_utils.ConvertTree(t)
