#!/usr/bin/env python
import script_util as S
import redhawk
import redhawk.utils.key_value_store as KVStore
import redhawk.utils.util as U

import os
import optparse

usage = "%prog listfiles"
description = S.MakeStringFromTemplate(
"""List the files in the index (database).
The index is stored in the $db file, in either the current directory or
some parent directory.
""")

def Main(args):
  parser = optparse.OptionParser(usage, description=description)
  options, args = parser.parse_args(args)

  if len(args):
    parser.error("Extra options given. This command takes no options!")

  database_file = S.GetDatabase()

  if database_file is None:
    S.ExitWithError(S.MakeStringFromTemplate(
        "No database found. Maybe $prog init first?"))

  store = KVStore.KeyValueStore(database_file, redhawk.GetVersion())
  for i in store.GetKeys():
    print U.GetDBPathRelativeToCurrentDirectory(i)
  store.Close()
  return
