#!/usr/bin/env python

""" Traversal Algorithms for walking the AST."""

import redhawk.utils.util as U

def DFS(tree):
  queue = [tree]

  while queue:
    node = queue.pop() # Pop from the end
    queue.extend([x for x in U.Flatten(node.GetChildren()) if x is not None])
    if node != None:
      yield node
