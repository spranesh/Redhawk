#!/usr/bin/env python

import hashlib
import operator
import os
import sys
import traceback 


def AssertWithError(condition, error):
  """ If condition is false, exit with error."""
  if callable(condition):
    condition = condition()
  if not condition:
    ExitWithError(error)


def Concat(li):
  """ Concat :: [[a]] -> [a].
      similar to Haskell's concat."""
  return reduce(operator.concat, li)


def ExitWithError(error, backtrace=True):
  if backtrace:
    traceback.print_stack()
  sys.stderr.write("\n" + error + "\n")
  sys.exit(1)


def Flatten(li):
  """ Returns a generator that is a flattened out version of the original
      list.
      Example:
        Flatten([1, 2, [3, 4]])     ->  [1, 2, 3, 4]
        Flatten([[1, [2]], [3, 4]]) ->  [1, 2, 3, 4]
  """
  for x in li:
    if type(x) == list:
      Flatten(x)
    else:
      yield x
  return


def GetHashDigest(filename):
  """ Get the sha1 digest of `filename`)"""
  try:
    fp = open(filename)
    digest = hashlib.sha1(fp.read()).hexdigest()
    fp.close()
    return digest
  except IOError, e:
    sys.stderr.write(e)
    sys.exit(1)
  return


def GuessLanguage(filename):
  """ Attempts to Guess Langauge of `filename`. Essentially, we do a
  filename.rsplit('.', 1), and a lookup into a dictionary of extensions."""
  try:
    (_, extension) = filename.rsplit('.', 1)
  except ValueError:
    ExitWithError("Could not guess language as '%s' does not have an \
        extension"%filename)

  return {'c'   : 'c'
         ,'py'  : 'python'}[extension]



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


def LogWarning(s, stream=sys.stderr):
  """ Log a warning to `stream` (default: sys.stderr.)"""
  stream.write("[WARNING]: %s\n"%(s))
  return


def StartShell(local_vars, banner=''):
  """ Start a shell, with the given local variables. It prints the given
  banner as a welcome message."""

  try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell.set_banner(banner)
    ipshell(local_ns=local_vars)
  except ImportError:
    import code
    code.interact(local=local_vars, banner=banner)
