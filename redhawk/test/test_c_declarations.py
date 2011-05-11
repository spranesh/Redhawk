#!/usr/bin/env python

""" Test various kinds of declarations.
    Declarations are present in the declarations.c file.

    Note that these tests only check that conversion works, and not that the
    resultant tree is actually correct (yet)."""

import c_test_utils as CT

TEST_FILE = "declarations.c"

test_descriptions = open("%s/%s"%(CT.RELATIVE_TEST_PATH, TEST_FILE)).readlines()

ConvertDeclaration = CT.ConvertTree

def TestDeclarations():
  t = CT.SetUp(TEST_FILE)
  for (i, description) in enumerate(test_descriptions):
    ConvertDeclaration.description = "Test `%s`"%(description.strip())
    yield ConvertDeclaration, t.children()[i]
