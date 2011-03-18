import redhawk.c.c_tree_converter as C
import redhawk.common.utils.misc_utils as U

import pycparser

import sys

RELATIVE_TEST_PATH = "c/tests/c_files/"
PICKLE_FILE = "c/tests/c_parsed.pickle"
  
def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  """ SetUp returns a parsed C Program."""
  return GetCASTFromDatabaseOrFile(rel_path + filename)

def ConvertTree(t, filename=None, verbose=True):
  """ Convert the C-AST into the L-AST."""
  if verbose:
    t.show()
  c = C.CTreeConverter(filename)
  ast = c.ConvertTree(t)
  if verbose:
    print ast.ToStr(), "\n\n"
  return ast

def GetCASTFromDatabaseOrFile(filename):
  """ Gets the parsed AST from either the pickle database or by parsing the
      file."""
  return U.ExtractASTFromDatabase(filename,
                                  PICKLE_FILE,
                                  ParseC)

def ParseC(filename):
  """ Parse the file using pycparser and return the parsed AST."""
  try:
    tree = pycparser.parse_file(filename, use_cpp = True)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)
  return tree

