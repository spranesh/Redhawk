#!/usr/bin/env python
import node
import node_position

def TestNodeInit():
  try:
    n = node.Node()
  except NotImplementedError, e:
    return
  assert(False)

