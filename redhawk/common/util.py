#!/usr/bin/env python

import cStringIO
import sys

def AssertWithError(condition, error):
  if callable(condition):
    condition = condition()
  if not condition:
    sys.stderr.write(error + "\n")
    sys.exit(1)

def LogWarning(s):
  sys.stderr.write("[WARNING]: %s\n"%(s))
  return

class CodeGeneratorBackend:
  """ A class to help code generation by managing indents."""
  def __init__(self, tab="  "):
    self.code = []
    self.tab = tab
    self.level = 0
    self.should_indent = True

  def GetCode(self):
    return "".join(self.code)

  def NewLine(self):
    self.code.append("\n")
    self.should_indent = True

  def Write(self, s):
    if self.should_indent:
      self.code.append(self.tab * self.level)
      self.should_indent = False
    self.code.append(s)
  
  def WriteLine(self, s):
    self.code.append(self.tab * self.level + s + "\n")

  def Indent(self):
    self.level = self.level + 1

  def Dedent(self):
    if self.level == 0:
      raise SyntaxError, "internal error in code generator"
    self.level = self.level - 1
