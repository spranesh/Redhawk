#!/usr/bin/env python
import script_util as S

import os
import optparse

usage = S.MakeStringFromTemplate("""
$prog init

This command is used to create an empty index in the CURRENT directory.
It takes no command line options. The AST index is stored in a file called
$db.
""")

def Main(args):
  parser = optparse.OptionParser(usage)
  options, args = parser.parse_args(args)

  if len(args):
    parser.error("Extra options given. This command takes no options!")

  if os.path.exists(S.DB_NAME):
    S.ExitWithError("An AST index already exists.")

  try:
    fp = open(S.DB_NAME, "w")
    fp.write("")
    fp.close()
  except IOError, e:
    S.ExitWithError(e)
  return
