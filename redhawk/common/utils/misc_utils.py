#!/usr/bin/env python

import hashlib
import os
import pickle as P
import sys

def AssertWithError(condition, error):
  """ If condition is false, exit with error."""
  if callable(condition):
    condition = condition()
  if not condition:
    sys.stderr.write(error + "\n")
    sys.exit(1)


def LogWarning(s):
  """ Log a warning to sys.stderr."""
  sys.stderr.write("[WARNING]: %s\n"%(s))
  return


def IfElse(condition, iftrue, iffalse):
  """ A re-implementation of C's ternary operator:
        Pass callables to avoid evaulation."""

  def CallIfPossible(x):
    if callable(x):
      return x()
    else:
      return x

  if CallIfPossible(condition):
    return CallIfPossible(iftrue)
  else:
    return CallIfPossible(iffalse)


def GetHashDigest(filename):
  try:
    fp = open(filename)
    digest = hashlib.sha1(fp.read()).hexdigest()
    fp.close()
    return digest
  except IOError, e:
    sys.stderr.write(e)
    sys.exit(1)
  return


def ExtractASTFromDatabase(filename, pickle_file,
    parser=None,
    key=''):
  """ Extract the parsed filename program from the pickle_file (a small
      database of sorts). The `pickle_file` stores a dictionary of keys
      (basenames by default) to a pair (digest, ast).

      If the program is not present or its sha1 sum has changed, use the function `parser` to parse the
      file. If parser is None, None is returned.

      The filename should be relative to the test root directory(redhawk/redhawk)
      Example:
        c/tests/c_files/prog001.c
  """
  
  digest = GetHashDigest(filename)

  try:
    fp = open(pickle_file)
    parsed_data = P.load(fp)
    fp.close()
  except (IOError, EOFError):
    parsed_data = {}

  basefile_name = key or os.path.basename(filename)

  if parsed_data.has_key(basefile_name):
    (pickled_digest, pickled_ast) = parsed_data[basefile_name]
    if pickled_digest == digest:
      return pickled_ast

  if parser is None:
    return None

  ast = parser(filename)
  parsed_data[basefile_name] = (digest, ast)

  fp = open(pickle_file, "w")
  P.dump(parsed_data, fp)
  fp.close()
  return ast
