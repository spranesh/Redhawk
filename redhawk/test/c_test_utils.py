""" A utilty module for C tests. """

import redhawk
import redhawk.c.c_tree_converter as C
import redhawk.common.get_ast as G
import redhawk.utils.key_value_store as KVStore

import os
import sys

RELATIVE_TEST_PATH = "test/files/c/"
PICKLE_FILE = "test/files/asts_c.redhawk_db"
  
def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  """ SetUp returns a parsed C Program."""
  if not os.path.exists(PICKLE_FILE):
    KVStore.CreateNewStore(PICKLE_FILE, redhawk.GetVersion())
  return G.GetLanguageSpecificTree(os.path.join(rel_path, filename),
      PICKLE_FILE, language='c')


def ConvertTree(t, filename=None, verbose=True):
  """ Convert the C-AST into the L-AST."""
  if verbose:
    t.show()
  c = C.CTreeConverter(filename)
  ast = c.Convert(t)
  if verbose:
    print ast.ToStr(), "\n\n"
  return ast

