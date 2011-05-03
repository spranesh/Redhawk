#!/usr/bin/env python

import redhawk.common.writers.xml_writer as X
import redhawk.common.test_utils as T

import nose.tools

import random
import itertools
import tempfile
import os.path

class TestXMLWriter:
  def __init__(self):
    self.counter = itertools.count(0)
    self.temp_dir = tempfile.mkdtemp(prefix='xml')
    return

  def GetFilename(self):
    i = self.counter.next()
    return os.path.join(self.temp_dir, str(i))

  def FunctionTestXML(self, ast):
    v = self.GetFilename()
    X.WriteToFile(ast, filename = v + '.xml')
    return


def TestGenerator():
  """ Testing XML Writer. """
  PICK=5
  c = TestXMLWriter()
  all_asts = list(T.GetAllLASTs())
  for i in range(PICK):
    r_index = random.randrange(0, len(all_asts))
    c.FunctionTestXML.im_func.description = "Test Random AST (%d) with XML Writer."%(r_index)
    yield c.FunctionTestXML, all_asts[r_index]


# Disable the test by default.
@nose.tools.nottest
def TestAllPrograms():
  """ Testing XML Writer (all programs) """
  c = TestXMLWriter()
  all_asts = list(T.GetAllLASTs())
  for (i, ast) in enumerate(all_asts):
    c.FunctionTestXML.im_func.description = "Testing AST (%d) with XML Writer."%(i)
    yield c.FunctionTestXML, ast

