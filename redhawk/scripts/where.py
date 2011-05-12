
#!/usr/bin/env python
import script_util as S
import redhawk.utils.key_value_store as KVStore
import redhawk

import os
import optparse

usage = S.MakeStringFromTemplate("""
$prog where

This command prints where the redhawk index (database) is located. The redhawk
index is stored in $db.
""")

def Main(args):
  parser = optparse.OptionParser(usage)
  options, args = parser.parse_args(args)

  if len(args):
    parser.error("Extra options given. This command takes no options!")

  database_file = S.GetDatabase()
  if database_file == None:
    print "No Index found."
  else:
    print database_file

  return
