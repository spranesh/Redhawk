#!/usr/bin/env python
""" Test initialising of the Node class in redhawk/common/node.py"""
from __future__ import absolute_import
import redhawk.common.node as node

def TestNodeInit():
  """ Test Node cannot be initialised. """
  try:
    n = node.Node()
  except NotImplementedError as e:
    return
  assert(False)

