#!/usr/bin/env python

""" Test Expressions """

from __future__ import absolute_import
from . import c_test_utils as CT

TEST_FILE = "expressions.c"

# Leave out the first two lines void f(),  { and the last }
test_descriptions = open("%s/%s"%(CT.RELATIVE_TEST_PATH,
  TEST_FILE)).readlines()[2:-1]

ConvertTree = CT.ConvertTree

def TestExpressions():
  t = CT.SetUp(TEST_FILE)
  for (i, description) in enumerate(test_descriptions):
    ConvertTree.description = "Test `%s`"%(description.strip())
    yield ConvertTree, t.ext[0].body.block_items[i]
