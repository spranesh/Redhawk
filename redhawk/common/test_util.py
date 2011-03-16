import util

class TestCodeGeneratorBackend:
  def setUp(self):
    self.c = util.CodeGeneratorBackend()

  def TestWrite(self):
    self.c.Write("a")
    self.c.Write(" = ")
    self.c.Write("b")
    assert(self.c.GetCode() == "a = b")

  def TestGetCode(self):
    self.c.Write("a")
    assert(self.c.GetCode() == "a")

  def TestWriteLine(self):
    self.c.WriteLine("print")
    self.c.WriteLine("print")
    assert(self.c.GetCode() == "print\nprint\n")

  def TestIndent(self):
    self.c.WriteLine("def Blah():")
    self.c.Indent()
    self.c.WriteLine("a = 2")
    assert(self.c.GetCode() == "def Blah():\n  a = 2\n")

  def TestDedent(self):
    self.c.Indent()
    self.c.WriteLine("a = 2")
    self.c.Dedent()
    self.c.WriteLine("return")
    assert(self.c.GetCode() == "  a = 2\nreturn\n")

  def TestEndToEnd(self):
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
