#!/usr/bin/env python
from __future__ import absolute_import
from . import script_util as S
import redhawk.utils.key_value_store as KVStore
import redhawk

import os
import optparse

usage = "%prog init"
description = S.MakeStringFromTemplate(
"""Create an empty LAST index in the CURRENT directory.  The LAST index is
stored in $db.""")

def Main(args):
  parser = optparse.OptionParser(usage, description=description)
  options, args = parser.parse_args(args)

  if len(args):
    parser.error("Extra options given. This command takes no options!")

  if os.path.exists(S.DB_NAME):
    S.ExitWithError("An AST index already exists.")

  KVStore.CreateNewStore(redhawk.GetDBName(), redhawk.GetVersion())
  return
