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

  database_file = S.GetDatabase()

  if database_file is None:
    S.ExitWithError(S.MakeStringFromTemplate(
        "No database found. Maybe $prog init first?"))

  ast_fetcher = G.CreateLASTFetcher(database_file, store_new = True)
  for f in S.GetSupportedFiles(args):
    ast = ast_fetcher.GetAST(f, key=S.GetKey(f, database_file))
    print "%s: Parsing "%(f)
  print "Adding to Database.."
  ast_fetcher.Close()
  print "Done"
  return
