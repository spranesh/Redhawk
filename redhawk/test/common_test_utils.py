#!/usr/bin/env python

import redhawk.utils.get_ast as G
import redhawk.utils.parse_asts as P

import os
import glob

AST_FILES = [("test/files/c/*.c", 'c', 'test/files/asts_c.pickle')
            ,("test/files/python/*.py", 'python', 'test/files/asts_python.pickle')]

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


if __name__ == '__main__':
  files_found = list(GetAllLASTs())
  print "Files Found:"
  for x in files_found:
    print x, x.filename
