#!/usr/bin/env python

import sys

def AssertWithError(condition, error):
  """ If condition is false, exit with error."""
  if callable(condition):
    condition = condition()
  if not condition:
    sys.stderr.write(error + "\n")
    sys.exit(1)


def LogWarning(s):
  """ Log a warning to sys.stderr."""
  sys.stderr.write("[WARNING]: %s\n"%(s))
  return


def IfElse(condition, iftrue, iffalse):
  """ A re-implementation of C's ternary operator:
        Pass callables to avoid evaulation."""

  def CallIfPossible(x):
    if callable(x):
      return x()
    else:
      return x

  if CallIfPossible(condition):
    return CallIfPossible(iftrue)
  else:
    return CallIfPossible(iffalse)

