#!/usr/bin/env python
""" Test initialising of the Node class in redhawk/common/node.py"""
import redhawk.common.node as node

def TestNodeInit():
  """ Test Node cannot be initialised. """
  try:
    n = node.Node()
  except NotImplementedError, e:
    return
  assert(False)

