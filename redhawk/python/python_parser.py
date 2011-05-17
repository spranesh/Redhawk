#!/usr/bin/env python
""" Implementation of the Python Parser class."""
import python_tree_converter
import redhawk.common.parser as parser

import ast
import logging

class PythonParser(parser.Parser):
  def GetTreeConverterClass(self):
    return python_tree_converter.PythonTreeConverter

  def Parse(self, filename):
    """ Parse a Python file using the ast module and return the Python AST."""
    try:
      tree = ast.parse(open(filename).read(), filename = filename)
      return tree
    except SyntaxError, e:
      error = "Error parsing file %s with ast module. Skipping\n"%(filename)
      logging.warning(error)
      return None
