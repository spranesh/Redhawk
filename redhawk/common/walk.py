#!/usr/bin/env python

def Walk(node):
  for n in node.GetChildren():
    yield n
    Walk(n)
