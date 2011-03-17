#!/usr/bin/env python

import cStringIO
import functools
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


def CreateStringFromList(words, level_space, indent_level):
  leading_whitespace = " " * (level_space * indent_level)
  if type(words) is str:
    return leading_whitespace + words
  stream = cStringIO.StringIO()
  stream.write(leading_whitespace)
  stream.write("(")
  for (i, w) in enumerate(words):
    if type(w) is str:
      stream.write(w)

    elif type(w) is list:
      stream.write("\n")
      stream.write(CreateStringFromList(w, level_space, 
        indent_level+1))

    elif isinstance(w, N.Node):
      if i is not 0:
        s = w.ToStr(indent_level+1)
        stream.write("\n")
      else:
        s = w.ToStr()
      stream.write(s)

    else:
      stream.write(str(w))
    stream.write(" ")

  return stream.getvalue()[:-1] + ")"


def ConvertToStringWithIndent(f, level_space = 2):

  def Wrapper(self, indent_level=0):
    words = f(self, indent_level)
    assert(len(words) is not 0)

    return CreateStringFromList(words, level_space, indent_level)

  return functools.update_wrapper(Wrapper, f)

