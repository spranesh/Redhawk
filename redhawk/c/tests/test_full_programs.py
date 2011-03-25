#!/usr/bin/env python

""" Tests conversion of full programs. """

import test_utils

tests = [("prog001.c", "Function to return 0")
        ,("prog002.c", "Static function to return 0")
        ,("prog003.c", "An expression")
        ,("prog004.c", "Variable Declaration")
        ,("prog005.c", "Pointer Declaration")
        ,("prog006.c", "Pointer to array of chars")
        ,("prog007.c", "Assignment Statements")
        ,("prog008.c", "Function Call")
        ,("prog009.c", "Linked List Structure")
        ,("prog010.c", "If Else - Rec. Fibonacci")
        ,("prog011.c", "For Loop - Iter. Fibonacci")
        ,("prog012.c", "While Loop - Factorial")
        ,("prog013.c", "Do While Loop - Factorial")
        ,("prog014.c", "Switch Case - isspace")
        ,("prog015.c", "Cast - To Char *")
        ,("prog016.c", "Test Typedefs")
        ,("prog017.c", "Test Full Programs")
        ,("prog018.c", "Test Enum")
        ,("prog019.c", "Test Ellipsis Parameters")
        ,("prog020.c", "Test Break and Continue")
        ,("prog021.c", "Test Goto and Label")
        ,("prog022.c", "Test Union (decl and ref)")
        ,("prog023.c", "Test Structure Defintion")]

def ConvertFile(filename):
  t = test_utils.SetUp(filename)
  return test_utils.ConvertTree(t)

def TestPrograms():
  for (filename, description) in tests:
    ConvertFile.description = "Test %s (%s)"%(filename, description)
    yield ConvertFile, filename
