#!/usr/bin/env python
import node
import node_position

def TestNodeInit():
  """ Test Node cannot be initialised. """
  try:
    n = node.Node()
  except NotImplementedError, e:
    return
  assert(False)

