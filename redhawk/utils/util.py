#!/usr/bin/env python
import redhawk

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
  flat = []
  for x in li:
    if type(x) == list:
      flat.extend(Flatten(x))
    else:
      flat.append(x)
  return flat


def GetHashDigest(filename):
  """ Get the sha1 digest of `filename`)"""
  try:
    fp = open(filename)
    digest = hashlib.sha1(fp.read()).hexdigest()
    fp.close()
    return digest
  except IOError, e:
    sys.stderr.write(str(e))
    sys.exit(1)
  return


def GuessLanguage(filename):
  """ Attempts to Guess Langauge of `filename`. Essentially, we do a
  filename.rsplit('.', 1), and a lookup into a dictionary of extensions."""
  try:
    (_, extension) = filename.rsplit('.', 1)
  except ValueError:
    raise ValueError("Could not guess language as '%s' does not have an \
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
    from IPython.Shell import IPShell
    ipshell = IPShell(user_ns = local_vars)
    ipshell.mainloop(banner)
  except ImportError:
    import readline, rlcompleter, code 
    readline.parse_and_bind("tab: complete")
    readline.set_completer(rlcompleter.Completer(local_vars).complete)
    code.interact(local=local_vars, banner=banner)


def FindFileInDirectoryOrAncestors(filename, dirname, perm=os.R_OK | os.W_OK):
  """ Tries to find the file `filename` in the given directory `dirname` or
  its parents. When found it makes sure the permissions match the given
  `perm`. If no file is found, None is returned. If the file was found, but
  the permissions are not satisfied, it raises an IOError."""
  dirname = os.path.abspath(dirname)

  while not os.path.exists(os.path.join(dirname, filename)):
    parent_dirname = os.path.dirname(dirname)
    if dirname == parent_dirname:
      return None
    dirname = parent_dirname

  filepath = os.path.join(dirname, filename)
  if os.access(filepath, perm) is False:
    raise IOError("Read write permissions deny access to file %s"%(filepath))

  return filepath


def AdjustFilePathToBaseDirectory(filepath, base_dir):
  """ Adjust filepath, `filepath` to base directory, `base_dir`.
  This function for example, on inputs
    filepath = '/a/b/c/d.txt', base_dir = '/a/b'
  returns 'c/d.txt'

  If either the filepath nor the base_dir passed in is not in its absolutized
  normalized form, it is taken to be relative to the current directory
  (pwd)."""

  return os.path.relpath(filepath, base_dir)

  print filepath
  print cur_dir

def GetDBPathRelativeToCurrentDirectory(filepath):
  database_dir = os.path.dirname(
      FindFileInDirectoryOrAncestors(
        redhawk.GetDBName(),
        os.curdir))

  abs_filepath = os.path.join(database_dir, filepath)
  return os.path.relpath(abs_filepath, os.curdir)

def OpenSourceFile(filepath):
  """ Try to open the file. If not, we try to open the filepath as one
  relative to the redhawk database."""
  try:
    return open(filepath)
  except IOError, e:
    pass
  
  return open(GetDBPathRelativeToCurrentDirectory(filepath))
