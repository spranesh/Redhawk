#!/usr/bin/env python

""" Traversal Algorithms for walking the AST."""

import redhawk.utils.util as U
from collections import deque

def DFS(tree):
  queue = deque([tree])

  while queue:
    node = queue.pop() # Pop from the end
    if node:
      for x in node.GetFlattenedChildren():
        if x is not None:
          queue.append(x)
      yield node
