import redhawk.c.c_tree_converter as C

import pycparser

import sys

RELATIVE_TEST_PATH = "c/tests/c_files/"

def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  """ Parse the file using pycparser and return the parsed AST."""
  filename = rel_path + filename
  try:
    tree = pycparser.parse_file(filename, use_cpp = True)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)
  # print open(filename).read()
  return tree


def ConvertTree(t, filename=None):
  """ Convert the C-AST into the L-AST."""
  t.show()
  c = C.CTreeConverter(filename)
  ast = c.ConvertTree(t)
  print ast, "\n\n"
  return ast
