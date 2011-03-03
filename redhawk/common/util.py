#!/usr/bin/env python
import node as N

import functools
import cStringIO

def ConvertToStringWithIndent(f, level_space = 2):

  def Wrapper(self, indent_level=0):
    stream = cStringIO.StringIO()
    words = f(self, indent_level)
    assert(len(words) is not 0)

    leading_whitespace = " " * (indent_level * level_space)

    stream.write(leading_whitespace)
    stream.write("(")
    for w in words:
      if type(w) is str:
        stream.write(w)
      elif isinstance(w, N.Node):
        s = w.ToStr(indent_level+1)
        stream.write("\n")
        stream.write(s)
      else:
        stream.write(leading_whitespace)
        stream.write(str(w))
      stream.write(" ")

    return stream.getvalue()[:-1] + ")"

  return functools.update_wrapper(Wrapper, f)

