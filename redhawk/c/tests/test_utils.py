""" A utilty module for C tests. """

import redhawk.c.c_tree_converter as C
import redhawk.utils.get_ast as G

import pycparser

import sys

RELATIVE_TEST_PATH = "c/tests/c_files/"
PICKLE_FILE = "c/tests/c_parsed.pickle"
  
def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  """ SetUp returns a parsed C Program."""
  return G.GetLanguageSpecificTree(rel_path + filename, PICKLE_FILE, language='c')


def ConvertTree(t, filename=None, verbose=True):
  """ Convert the C-AST into the L-AST."""
  if verbose:
    t.show()
  c = C.CTreeConverter(filename)
  ast = c.Convert(t)
  if verbose:
    print ast.ToStr(), "\n\n"
  return ast

