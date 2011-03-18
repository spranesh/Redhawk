#!/usr/bin/env python

import redhawk.c.tests.test_utils as CU

import glob

def ConvertCProgram(filename):
  t = CU.GetCASTFromDatabaseOrFile(filename)
  return CU.ConvertTree(t)

def ConvertPythonProgram(filename):
  pass


AST_FILES_AND_CONVERTERS = [
    ("c/tests/c_files/*.c", ConvertCProgram)
]

def GetAllLASTs():
  for (g, f) in AST_FILES_AND_CONVERTERS:
    for filename in glob.glob(g):
      yield f(filename)

def TestGetAllLASTs():
  count = 0
  for i in GetAllLASTs():
    count += 1
    print "." ,

  print
  print count
  return

