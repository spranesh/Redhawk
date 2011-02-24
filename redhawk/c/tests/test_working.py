#!/usr/bin/env python

""" Tests whether all the transformations are in place to convert the
programs. """

import redhawk.c.c_tree_converter as C

import pycparser

import sys

def ConvertProgram(filename, rel_path="redhawk/c/tests/"):
  try:
    tree = pycparser.parse_file(rel_path + filename)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)

  converter = C.CTreeConverter()

  t = converter.ConvertTree(tree)

  print t
  return

def Test001(): ConvertProgram("prog001.c")

