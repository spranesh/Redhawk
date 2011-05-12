#!/usr/bin/env python

""" Helper Functions for obtaining and printing the current position.

Most users will either just use ContextInFile or PrintContextInFile.

In case one wants to get the position first, and print it, a composition of
GetPosition, and ShowPosition will be useful.
"""

def ContextInFile(tree, context = 3, lines=None):
  """ Return the lines (with context) of the tree in its file."""
  return ShowPosition(GetPosition(tree), context=context, lines=lines)


def PrintContextInFile(tree, context = 3, lines = None):
  """ Print the context of the tree in its file."""
  print ContextInFile(tree, context, lines)
  return


def GetPosition(tree):
  """ Get the position of a node, of the position of its closest parent."""
  while (tree != None) and ((not hasattr(tree, 'position')) or (tree.position
    == None)):
    tree = tree.GetParent()

  if tree == None:
    return None

  return tree.position


def ShowPosition(position, context = 3, formatted=True, lines = None):
  """ Show the position in some file."""
  (f, l, c) = position.GetFile(), position.GetLine(), position.GetColumn()
  assert(position != None)

  return __FormatResult(f, l-1, context, lines)


def __FormatResult(filepath, line_index, context=3, lines = None):
  """ Format the result in a fashion similar to grep. Line numbers passed to
  this function (line_index) start from 0.

  If context is 0, the usual one-line grep syntax is returned.
  Otherwise the context is returned using FormatLine for each line, and the
  current line is highlighted.
  
  The lines in the file can be optionally passed in for performance."""

  # If modules are found (the file itself), return only the filename.
  if line_index is -1:
    return "%s:0:"%(filepath)

  if lines is None:
    fp = open(filepath)
    lines = fp.readlines()
    fp.close()

  if len(lines) is 0:
    return "%s:0:"%(filepath)

  if context is 0:
    return "%s:%d:%s"%(filepath, line_index+1, lines[line_index].strip())

  # When there is a context
  max_line_number_size = len(str(line_index+context+1)) # Max line number length

  low  = max(line_index - context, 0)
  high = min(line_index + context+1, len(lines)-1)

  before = [__FormatLine(filepath, i, max_line_number_size, lines)
      for i in range(low,line_index)]

  after  = [__FormatLine(filepath, i, max_line_number_size, lines)
      for i in range(line_index+1,high)]

  current = __FormatLine(filepath, line_index, max_line_number_size,
      lines, highlight=True)

  return "".join(before + [current] + after)


def __FormatLine(filepath, line_index, max_line_number_size, lines, highlight = False):
  """ Format a single line."""
  if highlight:
    return "%s:%s: > %s"%(filepath, str(line_index+1).rjust(max_line_number_size), lines[line_index])
  else:
    return "%s:%s:   %s"%(filepath, str(line_index+1).rjust(max_line_number_size), lines[line_index])
