#!/usr/bin/env python

""" Test various kinds of declarations.
    Declarations are present in the declarations.c file.

    Note that these tests only check that conversion works, and not that the
    resultant tree is actually correct (yet)."""

import test_utils

TEST_FILE = "declarations.c"

test_descriptions = open("%s/%s"%(test_utils.RELATIVE_TEST_PATH, TEST_FILE)).readlines()

ConvertDeclaration = test_utils.ConvertTree

def TestDeclarations():
  t = test_utils.SetUp(TEST_FILE)
  for (i, description) in enumerate(test_descriptions):
    ConvertDeclaration.description = "Test `%s`"%(description.strip())
    yield ConvertDeclaration, t.children()[i]
