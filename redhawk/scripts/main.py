#!/usr/bin/env python
import script_util as S
import init
import add
import query
import prompt
import show

import optparse
import sys


HELP = S.MakeStringFromTemplate("""
Usage: $prog COMMAND [ARGS]

$prog - An AST based navigation system. 

The simplest use case is just:

  $ $prog query <query> files

Supported commands are:
  init        Create an EMPTY AST index.
  add         Add files to an AST index.
  query       Query for a pattern in a list of files, or in the index.
  prompt      Start a redhawk subshell, with preloaded modules, and parse-trees.
  show        Show (visualize) a file either as text, or as an image.

See $prog COMMAND --help for more detailed information about that command.

NOTE: The creation of an index for large projects is recommended. This can be
done with the init, and add commands.  Though recommended, an index is NOT
necessary.
""")

def Main():
  if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print HELP
    sys.exit(0)

  dispatch = { 
      'add':   add.Main,
      'init':  init.Main,
      'query': query.Main,
      'prompt': prompt.Main,
      'show':  show.Main,
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
