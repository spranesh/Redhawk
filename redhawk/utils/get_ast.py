#!/usr/bin/env python
""" This module contains procedures that are used to get Abstract Syntax
Trees. This module provides procedures that cache these ASTs (in pickled
files) of the user's choice, preventing unnecessary parsing, and tree
conversion.

The functions in this module are explained below. Note that whenever the
language argument is not passed, the GuessLanguage function from util.py is
used to guess the language.
    
    * GetLAst: This is the only function that the end user (generally)
      needs. This gets the languge agnostic ast of a given file. This is a
      wrapper around ExtractTreeFromDatabase. If key is None, the basename of
      the file passed is used.

    The following functions are generally NOT REQUIRED by the end user:

    * GetLanguageSpecificTree: This is similar to the GetLAst function,
      returns a language specific tree. This function can hence be used to retrieve (and cache)
      trees other than the Language Agnostic Tree. This function is used by
      the internal test suites. This is a wrapper around
      ExtractTreeFromDatabase. If key is none, the basename of the file passed
      is used.

    * ExtractTreeFromDatabase: This extracts a tree from the database,
      If the tree cannot be found, or its digest does not match, it parses the
      file using the parser, and stores it in the database. If key is none,
      the basename of the file passed is used.
"""

import parse_asts
import redhawk
import util

import cPickle as P
import os
import sys

VERSION_STRING = '__redhawk__version__'

def GetLAst(filename, pickle_file, key=None, language=None):
  """ Get the language agnostic AST from a cache (pickle_file)."""
  parser = lambda filename: parse_asts.GetLAst(filename, language)

  return ExtractTreeFromDatabase(filename = filename
                                ,parser = parser
                                ,pickle_file = pickle_file
                                ,key = key)


def GetLanguageSpecificTree(filename, pickle_file, key=None, language=None):
  """ Get a language SPECIFIC ast."""
  parser = lambda filename: parse_asts.ParseFile(filename, language)
  return ExtractTreeFromDatabase(filename = filename
                                ,parser = parser
                                ,pickle_file = pickle_file
                                ,key = key)



def ExtractTreeFromDatabase(filename, pickle_file, parser, key=None):
  """ Extract a tree from the databse, with the key `key`. If the tree cannot
  be found, or its digest does not match that of the `filename`'s use the
  parser to reparse the file, and store it in the databse.

  If key is none, the basename of the file is used.
  """
  if pickle_file is None:
    return parser(filename)

  digest = util.GetHashDigest(filename)
  
  key = key or os.path.basename(filename)

  try:
    fp = open(pickle_file)
    parsed_data = P.load(fp)
    fp.close()
  except (IOError, EOFError):
    sys.stderr.write("Could not read from database.\n")
    parsed_data = {}

  # If version numbers don't match, clear the pickle file.
  if (not parsed_data.has_key(VERSION_STRING) or
      parsed_data[VERSION_STRING] != redhawk.__version__):
    parsed_data = {}
    parsed_data[VERSION_STRING] = redhawk.__version__

  if parsed_data.has_key(key):
    (pickled_digest, pickled_ast) = parsed_data[key]
    if pickled_digest == digest:
      return pickled_ast

  if parser is None:
    return None

  ast = parser(filename)
  parsed_data[key] = (digest, ast)

  try:
    fp = open(pickle_file, "w")
    P.dump(parsed_data, fp)
    fp.close()
  except IOError, e:
    sys.stderr.write("Could not write to Database: No Write permissions?\n")
  return ast
