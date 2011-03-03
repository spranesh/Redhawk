import redhawk.c.c_tree_converter as C

import pycparser

import sys

def SetUp(filename, rel_path="c/tests/"):
  try:
    tree = pycparser.parse_file(rel_path + filename)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)

  return tree


def ConvertTree(t):
  c = C.CTreeConverter()
  t.show()
  ast = c.ConvertTree(t)
  print ast, "\n\n"
  return
