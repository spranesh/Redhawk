#!/usr/bin/env python
import script_util as S
import redhawk.common.selector as selector
import redhawk.common.format_position as format_position
import redhawk.common.get_ast as G
import redhawk.utils.util as U

import optparse
import os
import sys
import tempfile
import webbrowser

usage = "%prog prompt [OPTIONS] [FILE...]"
description = S.MakeStringFromTemplate(
"""Explore the LASTs using the Redhawk APIs in a python prompt. Use Help() in
the prompt for more help.""")

USE_DATABASE = False
STORE_NEW = False


def ConvertFileToAST(f):
  """ Convert a file into an language agnostic AST."""
  if USE_DATABASE:
    database = S.GetDatabase()
    return G.GetLAST(f, database, key=S.GetKey(f, database), store_new = STORE_NEW)
  else:
    return G.GetLAST(f, database=None)

def ConvertCodeToAST(s, language):
  """ Convert a code snippet into an language agnostic AST."""
  name = tempfile.mktemp(suffix='.' + language)
  fp = open(name, "w")
  fp.write(s)
  fp.close()
  return ConvertFileToAST(name)


def Main(args):
  global STORE_NEW
  parser = optparse.OptionParser(usage, description=description)
  parser.add_option(
      "-n",
      "--no-database",
      action="store_false",
      dest="no_db",
      default=False,
      help = "Explicity tell redhawk to NOT use the database." + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-s",
      "--store-new",
      action="store_true",
      dest="store_new",
      default=False,
      help = "Store new files that redhawk comes across in the database." + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "--no-ipython",
      action="store_true",
      dest="no_ipython",
      default=False,
      help = "Do not use IPython as a shell, even if installed."
      + S.OPTIONS_DEFAULT_STRING)


  options, args = parser.parse_args(args)

  database = None
  if options.no_db == False:
    database = S.GetDatabase()
    USE_DATABASE = True

  if options.store_new:
    STORE_NEW = True

  if args is []:
    trees = []
  else:
    ast_fetcher = G.CreateLASTFetcher(database, store_new = STORE_NEW)

    trees = []
    for f in S.GetSupportedFiles(args):
      trees.append(ast_fetcher.GetAST(f, key=S.GetKey(f, database)))
    ast_fetcher.Close()

  sys.argv = [] # So that IPython does not try to parse our options.
  return EnterShell(trees, try_ipython = not options.no_ipython)


def Help(display=True):
  s = """

Built in Variables:
    trees - contains the parse trees of the files passed in the command line

Built in Functions:
    ConvertFileToAst - Converts a file into a language agnostic AST.
    ConvertCodeToAst - Converts a code snippet into a language agnostic AST.
    Help             - Displays this prompt.
    ShowASTAsImage   - Shows the AST as a graph using dot.

Built in Modules:
    S - redhawk.common.selector 
    F - redhawk.common.format_position 

To view this again, use the Help() function.  """

  if display:
    print s
  else:
    return s
  

def EnterShell(trees, try_ipython):
  local_vars = {
      'trees' : trees,
      'ConvertFileToAST': ConvertFileToAST,
      'ConvertCodeToAST': ConvertCodeToAST,
      'Help':Help,
      'ShowASTAsImage':S.ShowASTAsImage,
      'S':selector,
      'F':format_position,
    }
  U.StartShell(
      local_vars,
      banner=Help(display=False),
      try_ipython = try_ipython)


if __name__ == '__main__':
  Main()
