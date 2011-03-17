#!/usr/bin/env python

import writer

import redhawk.common.utils.code_generator_backend as C

def WriteToScheme(tree):
  s = SchemeWriter()
  return s.WriteTree(tree)

class SchemeWriter(writer.Writer):
  def __init__(self, indent = '  '):
    self.code = C.CodeGeneratorBackend(tab = indent)
    return

  def WriteSExp(self, sexp, newline=True):
    if sexp is []:
      return

    if newline:
      self.code.NewLine()
      self.code.Indent()

    self.code.Write("(")

    for (i, s) in enumerate(sexp):
      if type(s) is list:
        if i == 0:
          self.WriteSExp(s,newline=False)
        else:
          self.WriteSExp(s)

      elif type(s) is str:
        self.code.Write(s)
        if i != len(sexp) - 1:
          self.code.Write(" ")

    self.code.Write(")")
    if newline:
      self.code.Dedent()
    return


  def WriteTree(self, tree):
    sexp = tree.GetRecursiveSExp()
    self.WriteSExp(sexp, newline=False)
    return self.code.GetCode()

