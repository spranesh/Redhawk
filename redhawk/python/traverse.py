#!/usr/bin/env python

""" Traversal Algorithms for walking the AST."""

def DFS(tree):
  for n in tree.GetFlattenedChildren():
    yield n
    DFS(n)
