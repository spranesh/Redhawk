#!/usr/bin/env python

""" Tests whether all the transformations are in place to convert the
programs. """

import redhawk.c.c_tree_converter as C

import pycparser

import sys

def SetUp(filename, rel_path="c/tests/"):
  try:
    tree = pycparser.parse_file(rel_path + filename)
  except StandardError, e:
    sys.stderr.write(str(e))
    assert(False)

  converter = C.CTreeConverter()
  return (converter, tree)


def ConvertProgram(filename):
  (c, t) = SetUp(filename)
  ast = c.ConvertTree(t)
  print ast
  return

def TestReturnConstant(): 
  (c, t) = SetUp("prog001.c")
  main = t.children()[0]
  return_node = main.body.block_items[0]
  ast = c.ConvertTree(return_node)
  print ast
  return

# def Test002(): ConvertProgram("prog002.c")
# def Test003(): ConvertProgram("prog003.c")
# def Test004(): ConvertProgram("prog004.c")

