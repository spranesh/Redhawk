#!/usr/bin/env python

import redhawk.common.get_ast as G
import redhawk.common.get_parser as P
import redhawk.utils.util as U

import os
import glob

AST_FILES = [("test/files/c/*.c", 'c', 'test/files/asts_c.redhawk_db')
            ,("test/files/python/*.py", 'python', 'test/files/asts_python.redhawk_db')]

def GetAllLASTs():
  for (g, language, database) in AST_FILES:
    for filename in glob.glob(g):
      yield GetLASTFromFile(filename, language, database)


def GetLASTFromFile(filename, language, database):
  """ We first fetch the tree's language specific AST, and use the Convert
  function of the parser returned by get_parser. This convoluted approach is
  taken since the language specific ASTs are cached by tests."""
  language_specific_tree = G.GetLanguageSpecificTree(filename
                                                    ,database
                                                    ,language=language
                                                    ,key = None)
  language = language or U.GuessLanguage(filename)
  return P.GetParser(language).Convert(language_specific_tree)

if __name__ == '__main__':
  files_found = list(GetAllLASTs())
  print "Files Found:"
  for x in files_found:
    print x, x.filename
