#!/usr/bin/env python
import node as N

import functools
import cStringIO

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

