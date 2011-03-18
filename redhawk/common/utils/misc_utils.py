#!/usr/bin/env python

import sys
import os
import pickle as P


def ExtractASTFromDatabase(filename, pickle_file, parser=None):
  """ Extract the parsed filename program from the pickle_file
      If the program is not present, use the function `parser` to parse the
      file. If parser is None, None is returned.

      The filename should be relative to the test root directory(redhawk/redhawk)
      Example:
        c/tests/c_files/prog001.c
  """
  try:
    fp = open(pickle_file)
    parsed_data = P.load(fp)
    fp.close()
  except (IOError, EOFError):
    parsed_data = {}

  basefile_name = os.path.basename(filename)
  if parsed_data.has_key(basefile_name):
    return parsed_data[basefile_name]

  if parser is None:
    return None

  print filename
  parsed_data[basefile_name] = parser(filename)
  fp = open(pickle_file, "w")
  P.dump(parsed_data, fp)
  fp.close()
  return parsed_data[basefile_name]


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

