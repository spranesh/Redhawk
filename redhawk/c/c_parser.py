#!/usr/bin/env python
""" Implementation of the C Parser class."""
from __future__ import absolute_import
from . import c_tree_converter
import redhawk.common.parser as parser

import pycparser

import os
import logging
import subprocess
import sys

class CParser(parser.Parser):
  def GetTreeConverterClass(self):
    return c_tree_converter.CTreeConverter

  def Parse(self, filename):
    """ Parse a C file by running it through the preprocessor, and pycparser and
    return the C AST."""
    fake_libc_dir = os.path.join(os.path.dirname(__file__), "fake_libc_include")

    preprocessor = [
      "cpp",
      "-I%s/"%(fake_libc_dir),
      '-U__GNUC__']

    # The following was a workaround dmalc.. suggested in Issue 11 in the
    # pycparser mailing list
    # Set CPP Flags to:
    #  [r'-D__attribute__(x)=',
    #   r'-D__asm__(x)=',
    #   r'-D__builtin_va_list=int', # just fake this
    #   r'-D__const=',
    #   r'-D__restrict=',
    #   r'-D__extension__=',
    #   r'-D__inline__=',
    #   ])

    preprocessor.append(filename)
    logging.debug(preprocessor)
    cpp = subprocess.Popen(
        args = preprocessor,
        stdout = subprocess.PIPE,
        stderr = sys.stderr,
        universal_newlines = True)

    cpp_text = cpp.stdout.read()
    return_code = cpp.wait()

    if return_code != 0:
      logging.debug("Return code for %s was %d"%(filename, return_code))

    try:
      parser = pycparser.c_parser.CParser()
      return parser.parse(cpp_text, filename)
    except pycparser.plyparser.ParseError as e:
      error = "Error parsing file %s with pycparser (with cpp). Skipping\n"%(filename)
      logging.warning(error)
      logging.debug(str(e))
      return None
