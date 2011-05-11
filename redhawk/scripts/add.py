#!/usr/bin/env python

import script_util as S
import redhawk.utils.get_ast as G

import optparse

usage = S.MakeStringFromTemplate("""
$prog add file1 ..

Add ASTs to the database.
(If a directory is given, it traverses it recursively.)
""")

def Main(args):
  parser = optparse.OptionParser(usage)
  options, args = parser.parse_args(args)

  if not len(args):
      parser.error("No files given.")

  database = S.GetDatabase()

  if database is None:
    S.ExitWithError(S.MakeStringFromTemplate(
        "No database found. Maybe $prog init first?"))

  ast_fetcher = G.CreateLASTFetcher(database)
  for f in S.GetSupportedFiles(args):
    ast = ast_fetcher.GetAST(f, key=S.GetKey(f, database))
    print "%s: Parsing "%(f)
  print "Adding to Database.."
  ast_fetcher.WriteDatabase()
  print "Done"
  return
