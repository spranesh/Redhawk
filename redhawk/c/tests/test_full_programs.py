#!/usr/bin/env python

""" Tests conversion of full programs. """

import test_utils

tests = [("prog001.c", "Function to return 0")
        ,("prog002.c", "Static function to return 0")
        ,("prog003.c", "An expression")
        ,("prog004.c", "Variable Declaration")
        ,("prog005.c", "Pointer Declaration")
        ,("prog006.c", "Point to array of chars")
        ,("prog007.c", "Assignment Statements")
        ,("prog008.c", "Function Call")
        ,("prog009.c", "Linked List Structure")
        ,("prog010.c", "If Else - Rec. Fibonacci")]

def ConvertFile(filename):
  t = test_utils.SetUp(filename)
  return test_utils.ConvertTree(t)

def TestPrograms():
  for (filename, description) in tests:
    ConvertFile.description = "Test %s (%s)"%(filename, description)
    yield ConvertFile, filename
