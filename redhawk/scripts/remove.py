#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
from . import script_util as S
import redhawk
import redhawk.common.get_ast as G
import redhawk.utils.util as U
import redhawk.utils.key_value_store as KVStore

import optparse

usage = "%prog remove [FILE...]"
description = S.MakeStringFromTemplate(
"""Remove LASTs of each FILE from the index (database).
If a directory is given, all the files in it are recursively removed from the
index.""")

def Main(args):
  parser = optparse.OptionParser(usage, description=description)
  options, args = parser.parse_args(args)

  if not len(args):
      parser.error("No files given.")

  database_file = S.GetDatabase()

  if database_file is None:
    S.ExitWithError(S.MakeStringFromTemplate(
        "No database found. Maybe $prog init first?"))

  store = KVStore.KeyValueStore(database_file, redhawk.GetVersion())
  for f in S.GetSupportedFiles(args):
    key = S.GetKey(f, database_file)
    if store.HasKey(key):
      print("Removing: %s"%(U.GetDBPathRelativeToCurrentDirectory(f)))
      store.RemoveKey(key)
    else:
      print("Not found: %s"%(U.GetDBPathRelativeToCurrentDirectory(f)))
  store.Close()
  return
