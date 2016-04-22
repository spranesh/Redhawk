#!/usr/bin/env python
""" Test the DotWriter module in redhawk/common/writers."""

from __future__ import absolute_import
import redhawk.common.writers.dot_writer as D
from . import common_test_utils as T

import nose.tools

import random
import itertools
import tempfile
import os

class TestDotWriter:
  def __init__(self):
    self.counter = itertools.count(0)
    self.temp_dir = tempfile.mkdtemp(prefix='images')
    return

  def GetFilename(self):
    i = next(self.counter)
    return os.path.join(self.temp_dir, str(i))

  def FunctionTestDot(self, ast):
    v = self.GetFilename()
    open(v + '.dot', "w").write(D.WriteToDot(ast))
    D.WriteToImage(ast, filename = v + '.png')
    return


test_dot_writer = TestDotWriter()

def TestGenerator():
  """ Testing Dot Writer. """
  PICK=1
  all_asts = list(T.GetAllLASTs())
  for i in range(PICK):
    r_index = random.randrange(0, len(all_asts))
    test_dot_writer.FunctionTestDot.__func__.description = "Test Random AST (%d) with Dot Writer."%(r_index)
    yield test_dot_writer.FunctionTestDot, all_asts[r_index]


def TestDotNewlineSupport():
  """ Test Dot for programs with newlines in keys/attr strings."""
  test_dot_writer.FunctionTestDot(T.GetLASTFromFile(
    "test/files/dot/newline.c", "c", None))
  test_dot_writer.FunctionTestDot(T.GetLASTFromFile(
    "test/files/dot/newline.py", "python", None))
  return


# Disable the test by default.
@nose.tools.nottest
def TestAllPrograms():
  """ Testing Dot Writer (all programs) """
  all_asts = list(T.GetAllLASTs())
  for (i, ast) in enumerate(all_asts):
    test_dot_writer.FunctionTestDot.__func__.description = "Testing AST (%d) with Dot Writer."%(i)
    yield test_dot_writer.FunctionTestDot, ast
