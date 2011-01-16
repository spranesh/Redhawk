""" The Node Class. """
import node_types

class Node:
  """ Signifies a node in the parse tree."""
  def __init__(self, type, properties={}, children={}, tags=[]):
    self.type = type
    self.properties = properties
    self.children = children
    self.tags = tags
    return
