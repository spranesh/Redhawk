import redhawk.python.python_tree_converter as P
import redhawk.utils.get_ast as G

import ast
import sys

RELATIVE_TEST_PATH = "python/tests/python_files/"
PICKLE_FILE = "python/tests/python_parsed.pickle"
  
def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  """ SetUp returns a parsed python Program."""
  return G.GetLanguageSpecificTree(rel_path + filename, PICKLE_FILE,
      language='python')


def ConvertTree(t, filename=None, verbose=True):
  """ Convert the C-AST into the L-AST."""
  if verbose:
    print ast.dump(t)
  c = P.PythonTreeConverter(filename)
  a = c.ConvertTree(t)
  if verbose:
    print a.ToStr(), "\n\n"
  return a

