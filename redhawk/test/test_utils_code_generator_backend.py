""" Test the code_generator_backend.py in redhawk/utils."""
from __future__ import absolute_import
import redhawk.utils.code_generator_backend as C

class TestCodeGeneratorBackend:
  def setUp(self):
    self.c = C.CodeGeneratorBackend()

  def TestWrite(self):
    """ Test CodeGeneratorBackend.Write."""
    self.c.Write("a")
    self.c.Write(" = ")
    self.c.Write("b")
    assert(self.c.GetCode() == "a = b")

  def TestGetCode(self):
    """ Test CodeGeneratorBackend.TestGetCode"""
    self.c.Write("a")
    assert(self.c.GetCode() == "a")

  def TestWriteLine(self):
    """ Test CodeGeneratorBackend.TestWriteLine"""
    self.c.WriteLine("print")
    self.c.WriteLine("print")
    assert(self.c.GetCode() == "print\nprint\n")

  def TestIndent(self):
    """ Test CodeGeneratorBackend.TestIndent"""
    self.c.WriteLine("def Blah():")
    self.c.Indent()
    self.c.WriteLine("a = 2")
    assert(self.c.GetCode() == "def Blah():\n  a = 2\n")

  def TestDedent(self):
    """ Test CodeGeneratorBackend.TestDedent"""
    self.c.Indent()
    self.c.WriteLine("a = 2")
    self.c.Dedent()
    self.c.WriteLine("return")
    assert(self.c.GetCode() == "  a = 2\nreturn\n")

  def TestEndToEnd(self):
    """ Test CodeGeneratorBackend.TestEndToEnd"""
    self.c.WriteLine("def Blah():")
    self.c.Indent()
    self.c.WriteLine("for i in range(3):")
    self.c.Indent()
    self.c.WriteLine("print i")
    self.c.Dedent()
    self.c.WriteLine("return 1")
    self.c.Dedent()
    assert(self.c.GetCode() == '\n'.join([
      "def Blah():",
      "  for i in range(3):",
      "    print i",
      "  return 1\n"]))
