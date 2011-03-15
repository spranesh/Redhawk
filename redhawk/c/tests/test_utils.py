import redhawk.c.c_tree_converter as C

import pycparser

import sys

RELATIVE_TEST_PATH = "c/tests/"

def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  filename = rel_path + filename
  try:
    tree = pycparser.parse_file(filename, use_cpp = True)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)
  # print open(filename).read()
  return tree


def ConvertTree(t, filename=None):
  t.show()
  c = C.CTreeConverter(filename)
  ast = c.ConvertTree(t)
  print ast, "\n\n"
  return
