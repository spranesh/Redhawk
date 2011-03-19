#!/usr/bin/env python

import redhawk.common.writers.dot_writer as D
import redhawk.common.test_utils as T

import nose.tools

import random
import itertools
import tempfile
import os.path

class TestDotWriter:
  def __init__(self):
    self.counter = itertools.count(0)
    self.temp_dir = tempfile.mkdtemp(prefix='images')
    return

  def GetFilename(self):
    i = self.counter.next()
    return os.path.join(self.temp_dir, str(i))

  def FunctionTestDot(self, ast):
    v = self.GetFilename()
    open(v + '.dot', "w").write(D.WriteToDot(ast))
    D.WriteToImage(ast, filename = v + '.png')
    return


def TestGenerator():
  """ Testing Dot Writer. """
  PICK=5
  c = TestDotWriter()
  all_asts = list(T.GetAllLASTs())
  for i in range(PICK):
    r_index = random.randrange(0, len(all_asts))
    c.FunctionTestDot.im_func.description = "Test Random AST (%d) with Dot Writer."%(r_index)
    yield c.FunctionTestDot, all_asts[r_index]


# Disable the test by default.
@nose.tools.nottest
def TestAllPrograms():
  """ Testing Dot Writer (all programs) """
  c = TestDotWriter()
  all_asts = list(T.GetAllLASTs())
  for (i, ast) in enumerate(all_asts):
    c.FunctionTestDot.im_func.description = "Testing AST (%d) with Dot Writer."%(i)
    yield c.FunctionTestDot, ast

