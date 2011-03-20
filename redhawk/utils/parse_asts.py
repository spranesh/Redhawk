#!/usr/bin/env python
""" This module contains functions that parse files and return asts. The
functions in this module should (generally) not be used directly. Instead, the
wrappers in redhawk/utils/get_last.py are to be used, as they also cache the
ASTs to store unnecessary parsing, and tree conversion.

      * GetLAst: Gets the Language Agnostic AST of a file. Essentially a
        function composition of ConvertAst and ParseFile.

      * ConvertAst: This function converts a language specific AST to the
        L-AST. This function takes an optional filename argument, to fill in
        the Module Node.



      The following functions are NOT required for external use:
      * ParseFile: This function delegates to the corresponding Parse
        function, using the language argument. If the language argument is
        None, utils.GuessLanguage is used.

      * ParsePython: This function parses Python files, and returns a
        python-ast. This function is generally not required for external use.

      * ParseC: This function parses C files, and returns a C-AST. This
        function is generally not required for external use.
"""

import redhawk.c.c_tree_converter as C
import util

import pycparser
import ast

def GetLAst(filename, language=None):
  """ Parse the file using the respective parser, and return the Language
  Agnostic AST."""

  return ConvertAst(ParseFile(filename, language)
                    ,language
                    ,filename)


def ConvertAst(ast, language, filename=None):
  if language == 'c':
    converter = C.CTreeConverter(filename)
  elif language == 'python':
    # converter = P.PythonTreeConverter(filename)
    raise NotImplementedError("Python converter not implemented.")
  else:
    raise NotImplementedError("Only C and Python Implemented so far")

  return converter.ConvertTree(ast)




# ####
# Functions that return Language Dependent ASTs

def ParseFile(filename, language=None):
  """ Parse the file using the respective parser, and return a Language
  SPECIFIC ast."""
  language_parsers = {'c'       : ParseC
                     ,'python'  : ParsePython}

  language = language or util.GuessLanguage(filename)
  return language_parsers[language](filename)


def ParseC(filename):
  """ Parse a C file using pycparser and return the C AST."""
  try:
    tree = pycparser.parse_file(filename, use_cpp = True)
  except StandardError, e:
    U.ExitWithError(str(e))
  return tree

def ParsePython(filename):
  """ Parse a Python file using the ast module and return the Python AST."""
  raise NotImplementedError("Python's not been implemented yet")

