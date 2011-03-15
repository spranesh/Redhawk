#!/usr/bin/env python

""" Test Expressions """

import test_utils

TEST_FILE = "expressions.c"

# Leave out the first two lines void f(),  { and the last }
test_descriptions = open("%s/%s"%(test_utils.RELATIVE_TEST_PATH,
  TEST_FILE)).readlines()[2:-1]

ConvertTree = test_utils.ConvertTree

def TestExpressions():
  t = test_utils.SetUp(TEST_FILE)
  for (i, description) in enumerate(test_descriptions):
    ConvertTree.description = "Test `%s`"%(description.strip())
    yield ConvertTree, t.children()[0].body.block_items[i]
