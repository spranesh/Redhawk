#!/usr/bin/env python

""" Base Writer class."""

class Writer:
  def __init__(self):
    return

  def WriteTree(self, tree):
    raise NotImplementedError("WriteTree is not implemented in the base class.")

  def WriteTreeToFile(self, tree, filename):
    fp = open(filename, "w")
    fp.write(self.WriteTree(tree))
    fp.close()
    return


