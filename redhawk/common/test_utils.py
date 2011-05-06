#!/usr/bin/env python

import redhawk.utils.get_ast as G
import redhawk.utils.parse_asts as P
import os

import glob

AST_FILES = [("c/tests/c_files/*.c", 'c', 'c/tests/c_parsed.pickle')
            ,("python/tests/*.py", 'python', 'python/tests/python_parsed.pickle')]

def GetAllLASTs():
  for (g, language, pickle_file) in AST_FILES:
    for filename in glob.glob(g):
      language_specific_tree = G.GetLanguageSpecificTree(filename
                                                        ,pickle_file
                                                        ,language=language
                                                        ,key = None)
      yield P.ConvertAst(language_specific_tree
                        ,language
                        ,filename)

def TestGetAllLASTs():
  """ Test the GetALLASTs function."""
  count = 0
  for i in GetAllLASTs():
    count += 1
    print "." ,

  print
  print count
  return

