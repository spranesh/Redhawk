#!/usr/bin/env python
""" Implementation of the C Parser class."""
import c_tree_converter
import redhawk.common.parser as parser

import pycparser

import os
import logging

class CParser(parser.Parser):
  def GetTreeConverterClass(self):
    return c_tree_converter.CTreeConverter

  def Parse(self, filename):
    """ Parse a C file by running it through the preprocessor, and pycparser and
    return the C AST."""
    fake_libc_dir = os.path.join(os.path.dirname(__file__), "fake_libc_include")

    try:
      tree = pycparser.parse_file(filename,
          use_cpp = True,
          cpp_path='cpp',
          cpp_args='-I%s/'%fake_libc_dir)
      return tree
    except pycparser.plyparser.ParseError, e:
      error = "Error parsing file %s with pycparser (with cpp). Skipping\n"%(filename)
      logging.warning(error)
      return None
