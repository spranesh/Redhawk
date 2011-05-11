#!/usr/bin/env python
import script_util as S
import redhawk.common.selector as selector
import redhawk.common.position as position
import redhawk.utils.get_ast as G
import redhawk.utils.util as U

import optparse
import os
import sys
import tempfile
import webbrowser

usage = S.MakeStringFromTemplate("""$prog prompt [options] file1 file2 ..

The prompt command is used to explore the ASTs, or for more complex queries
using the selector API.

Type help() at the prompt to know more.
""")

USE_DATABASE = False


def ConvertFileToAST(f):
  """ Convert a file into an language agnostic AST."""
  if USE_DATABASE:
    database = S.GetDatabase()
    return G.GetLAST(f, database, key=S.GetKey(f, database))
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
  parser = optparse.OptionParser(usage)
  parser.add_option(
      "-n",
      "--no-database",
      action="store_false",
      dest="use_db",
      default=True,
      help = "Explicity tell redhawk to NOT use the database." + S.OPTIONS_DEFAULT_STRING)

  options, args = parser.parse_args(args)

  database = None
  if options.use_db:
    database = S.GetDatabase()
    USE_DATABASE = True

  if args is []:
    trees = []
  else:
    ast_fetcher = G.CreateLASTFetcher(database)
    trees = [ast_fetcher.GetAST(f, key=S.GetKey(f, database)) for f in args]
    ast_fetcher.WriteDatabase()
  return EnterShell(trees)


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
    P - redhawk.common.position 

To view this again, use the Help function.  """

  if display:
    print s
  else:
    return s
  

def EnterShell(trees):
  local_vars = {
      'trees' : trees,
      'ConvertFileToAST': ConvertFileToAST,
      'ConvertCodeToAST': ConvertCodeToAST,
      'Help':Help,
      'ShowASTAsImage':S.ShowASTAsImage,
      'S':selector,
      'P':position,
    }
  U.StartShell(local_vars, banner=Help(display=False))


if __name__ == '__main__':
  Main()
