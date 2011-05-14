#!/usr/bin/env python
import script_util as S
import add
import init
import listfiles
import prompt
import query
import remove
import show
import where

import optparse
import sys


usage = S.MakeStringFromTemplate(
"""$prog [-v] COMMAND [OPTIONS] [ARGS...]

The simplest use case is just:

  $ $prog query <query> files

Supported commands are:

  init        Create an EMPTY AST index.
  add         Add files to an AST index.
  listfiles   List all the files in the AST index.
  prompt      Start a redhawk subshell, with preloaded modules, and parse-trees.
  query       Query for a pattern in a list of files, or in the index.
  remove      Remove files from the AST index.
  show        Show (visualize) a file either as text, or as an image.
  where       Print the location of the current redhawk index (if there is one).

See $prog COMMAND --help for more detailed information about that command.

NOTE: The creation of an index for large projects is recommended. This can be
done with the init, and add commands.  Though recommended, an index is NOT
necessary. """)

def Main():
  if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print usage
    sys.exit(0)

  if "-v" in sys.argv[1:] or "--version" in sys.argv[1:]:
    import redhawk
    print "Redhawk Version: v%s"%(redhawk.GetVersion())
    sys.exit(0)

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
  if sys.argv[1] in dispatch:
    dispatch[sys.argv[1]](sys.argv[2:])
  else:
    print "Command %s not found."%sys.argv[1]
    print HELP
    sys.exit(1)
  return


if __name__ == '__main__':
  Main()
