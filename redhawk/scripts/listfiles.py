#!/usr/bin/env python
import script_util as S
import redhawk
import redhawk.utils.key_value_store as KVStore
import redhawk.utils.util as U

import os
import optparse

usage = S.MakeStringFromTemplate("""
$prog listfiles

This command is used to list the files in the database. It takes no command
line options. The database is stored in a file called $db, in either the
current directory or some parent directory.
""")

def Main(args):
  parser = optparse.OptionParser(usage)
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
