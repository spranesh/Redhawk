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

