#!/usr/bin/env python

""" Test Conversions."""

import redhawk.python.python_tree_converter as P
import redhawk.utils.get_ast as G

import nose.tools

import ast
import glob
import sys

RELATIVE_TEST_PATH = "python/tests/"
  
def SetUp(filename, rel_path=RELATIVE_TEST_PATH):
  """ SetUp returns a parsed python Program."""
  PICKLE_FILE = "python/tests/python_parsed.pickle"
  return G.GetLanguageSpecificTree(rel_path + filename, PICKLE_FILE,
      language='python')


def ConvertTree(t, filename=None, verbose=True):
  """ Convert the Python-AST into the L-AST."""
  if verbose:
    print ast.dump(t)
  c = P.PythonTreeConverter(filename)
  a = c.ConvertTree(t)
  if verbose:
    print a.ToStr(), "\n\n"
  return a


def ReadLines(filename):
  return open("%s/%s"%(RELATIVE_TEST_PATH, filename)).readlines()


def CTWD(filename, description, backquote = True, verbose = True):
  """ Return the ConvertTree function after setting its description tag
  appropriately."""
  x = lambda t: ConvertTree(t, filename, verbose)
  if backquote:
    x.description = "Test [%s]:`%s`"%(filename, description.strip())
  else:
    x.description = "Test [%s]:%s"%(filename, description.strip())
  return x



def TestExpressions():
  filename = "expressions.py"
  t = SetUp(filename)
  test_descriptions = ReadLines(filename)[1:]

  for i in range(len(t.body)):
    yield CTWD(filename, test_descriptions[i]), t.body[i]


def TestStatements():
  filename = "statements.py"

  t = SetUp(filename)
  test_descriptions = ReadLines(filename)[1:]
  for i in range(len(t.body)):
    yield CTWD(filename, test_descriptions[i]), t.body[i]


def TestAllPrograms():
  filenames = glob.glob(RELATIVE_TEST_PATH + "*.py")
  filenames.sort()

  for f in filenames:
    description = open(f).readline().strip()
    if description[0] == '#':
      description = description[1:].strip()
    else:
      description = "---"

    t = SetUp(f, rel_path = "")
    yield CTWD(f, description, backquote=False),  t
