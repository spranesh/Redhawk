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
      yield GetLASTFromFile(filename, language, pickle_file)


def GetLASTFromFile(filename, language, pickle_file):
  """ We first fetch the tree's language specific AST, and use the ConvertAST
  function in parse_asts. This convoluted approach is taken since the language
  specific ASTs are cached by tests."""
  language_specific_tree = G.GetLanguageSpecificTree(filename
                                                    ,pickle_file
                                                    ,language=language
                                                    ,key = None)
  return P.ConvertAst(language_specific_tree
                        ,language
                        ,filename)
