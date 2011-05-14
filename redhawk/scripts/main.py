#!/usr/bin/env python
import add
import init
import listfiles
import prompt
import query
import remove
import show
import where

import redhawk
import script_util as S

import logging
import optparse
import sys


usage = "%prog [-h] [--version] [-v..] COMMAND [OPTIONS] [ARGS...]"
description = "A LAST based navigation system."
epilog = S.MakeStringFromTemplate(
"""
The simplest use case is just:

  $ $prog query <query> files

Supported commands are:

  init        Create an EMPTY LAST index.
  add         Add files to an LAST index.
  listfiles   List all the files in the LAST index.
  prompt      Start a redhawk subshell, with preloaded modules, and parse-trees.
  query       Query for a pattern in a list of files, or in the index.
  remove      Remove files from the AST index.
  show        Show (visualize) a file either as text, or as an image.
  where       Print the location of the current redhawk index (if there is one).

See $prog COMMAND --help for more detailed information about that command.

NOTE: The creation of an index for large projects is recommended. This can be
done with the init, and add commands.  Though recommended, an index is NOT
necessary. """)

def SplitArgs(d, args):
  s = len(args)
  for i in range(len(args)):
    if args[i] in d:
      s = i
      break

  return args[:s], args[s:]

def Main():
  dispatch = { 
      'add':   add.Main,
      'init':  init.Main,
      'listfiles': listfiles.Main,
      'prompt': prompt.Main,
      'query': query.Main,
      'remove': remove.Main,
      'show':  show.Main,
      'where': where.Main,
  }

  (main_args, dispatch_args) = SplitArgs(dispatch, sys.argv[1:])

  parser = optparse.OptionParser(
      usage = usage,
      description = description)

  parser.add_option(
      "-v",
      dest="verbose",
      action="count",
      default=1,
      help="Increase verbosity (specify multiple times for more)"
      + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      '--version',
      action="store_true",
      dest="version",
      default=False,
      help = "Print version and exit.")

  # Hack to get redhawk to show formatted help with optparse
  if len(sys.argv) == 1 or sys.argv[1] in "-h --help".split():
    parser.print_help()
    print epilog
    sys.exit(0)

  options, args = parser.parse_args(main_args)

  if len(args):
    parser.error("Unrecognised command: %s"%" ".join(args))

  if options.verbose == 1:
    log_level = logging.ERROR
  if options.verbose == 2:
    log_level = logging.WARNING
  if options.verbose == 3:
    log_level = logging.INFO
  if options.verbose == 4:
    log_level = logging.DEBUG

  logging.basicConfig(level=log_level)

  if options.version:
    print "Redhawk Version: v%s"%(redhawk.GetVersion())
    sys.exit(0)

  if len(dispatch_args) is 0:
    parser.error("No Commands given")

  if dispatch_args[0] in dispatch:
    dispatch[dispatch_args[0]](dispatch_args[1:])
  else:
    print "Command %s not found."%args[0]
    print usage
    sys.exit(1)
  return


if __name__ == '__main__':
  Main()
