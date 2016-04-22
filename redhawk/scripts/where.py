
#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from . import script_util as S
import redhawk.utils.key_value_store as KVStore
import redhawk

import os
import optparse

usage = "%prog where"
description = S.MakeStringFromTemplate(
"""Print where the redhawk index (database) is located. The redhawk index is
stored in $db.
""")

def Main(args):
  parser = optparse.OptionParser(usage, description=description)
  options, args = parser.parse_args(args)

  if len(args):
    parser.error("Extra options given. This command takes no options!")

  database_file = S.GetDatabase()
  if database_file == None:
    print("No Index found.")
  else:
    print(database_file)

  return
