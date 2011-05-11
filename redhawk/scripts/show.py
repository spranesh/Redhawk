#!/usr/bin/env python
""" Implementation of redhawk show"""
import script_util as S

import redhawk.utils.get_ast as G

import optparse
import os

usage = S.MakeStringFromTemplate("""$prog show [options] <query> <file>

This command is used to show an AST. An AST can either be printed (default),
or converted to an image (this requires python-graphviz).
""")


def Main(args):

  parser = optparse.OptionParser(usage)

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
      action="store_false",
      dest="use_db",
      default=True,
      help = "Explicity tell redhawk to NOT use the database." + S.OPTIONS_DEFAULT_STRING)

  options, args = parser.parse_args(args)
  if len(args) != 1:
      parser.error("Exactly one file should be given.")

  database = S.GetDatabase() if options.use_db else None


  ast = G.GetLAST(args[0], database = database, key=S.GetKey(args[0], database))
  if options.eog:
    options.image = True

  if not options.image:
    print ast.ToStr()

  else:
    S.ShowASTAsImage(ast, options.eog)
  return
