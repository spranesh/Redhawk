#!/usr/bin/env python

""" Helper Functions for obtaining the position."""

def GetPosition(tree):
  """ Get the position of a node, of the position of its closest parent."""
  while (tree != None) and (tree.position == None):
    tree = tree.GetParent()

  if tree == None:
    return None

  return tree.position


def ShowPosition(position, context = 3, formatted=True):
  """ Show the position in some file."""
  (f, l, c) = position.GetFile(), position.GetLine()-1, position.GetColumn()
  assert(position != None)

  fp = open(f)
  lines = fp.readlines()
  fp.close()

  if formatted:
    return HighlightCurrentLine(l, lines, context)
  else:
    return "".join(lines[l-context:l+context])


def HighlightCurrentLine(l, lines, context = 3):
  before = ["  " + x for x in lines[l-context:l]]
  after  = ["  " + x for x in lines[l+1:l+context]]
  line = "> " + lines[l]
  return "".join(before + [line] + after)
