import redhawk.c.c_tree_converter as C

import pycparser

import os.path
import pickle as P
import sys

RELATIVE_TEST_PATH = "c/tests/c_files/"
PICKLE_FILE = "c/tests/c_parsed.pickle"

def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  filename = rel_path + filename
  try:
    fp = open(PICKLE_FILE)
    parsed_data = P.load(fp)
    fp.close()
  except (IOError, EOFError):
    parsed_data = {}

  basefile_name = os.path.basename(filename)
  if parsed_data.has_key(basefile_name):
    return parsed_data[basefile_name]

  parsed_data[basefile_name] = ParseC(filename)
  fp = open(PICKLE_FILE, "w")
  P.dump(parsed_data, fp)
  fp.close()
  return parsed_data[basefile_name]
  

def ParseC(filename):
  """ Parse the file using pycparser and return the parsed AST."""
  try:
    tree = pycparser.parse_file(filename, use_cpp = True)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)
  return tree


def ConvertTree(t, filename=None):
  """ Convert the C-AST into the L-AST."""
  t.show()
  c = C.CTreeConverter(filename)
  ast = c.ConvertTree(t)
  print ast, "\n\n"
  return ast
