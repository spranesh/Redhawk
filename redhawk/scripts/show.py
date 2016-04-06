#!/usr/bin/env python
""" Implementation of redhawk show"""
from __future__ import absolute_import
from __future__ import print_function
from . import script_util as S

import redhawk.common.get_ast as G

import optparse
import os

usage = "%prog show [OPTIONS] FILE"
description = S.MakeStringFromTemplate(
"""Show or display an LAST. A LAST can either be printed (default), or
converted to an image (requires python-graphviz).""")


def Main(args):
  parser = optparse.OptionParser(usage, description=description)

  parser.add_option(
      "-e",
      "--eog",
      action="store_true",
      dest="eog",
      default=False,
      help = "Show the AST as an image using Eye-of-gnome. (assumes -i)" + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-i",
      "--image",
      action="store_true",
      dest="image",
      default=False,
      help = "Show the AST as an image." + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-n",
      "--no-database",
      action="store_true",
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

  options, args = parser.parse_args(args)
  if len(args) != 1:
      parser.error("Exactly one file should be given.")

  database_file = S.GetDatabase() if options.no_db == False else None


  ast_fetcher = G.CreateLASTFetcher(database_file, store_new = options.store_new)
  ast = ast_fetcher.GetAST(args[0], key=S.GetKey(args[0], database_file))
  ast_fetcher.Close()

  if options.eog:
    options.image = True

  if not options.image:
    print(ast.ToStr())

  else:
    S.ShowASTAsImage(ast, options.eog)
  return
