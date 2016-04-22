#!/usr/bin/env python

""" 
This API is meant to be a private API. It is encapsulated by the `S` class in
selector.py which is to be used by the outside world.

A selector is a function that selects some nodes of the AST depending on
some constraints. Selector functions have the type

    selector :: tree -> Bool

Three types of selector functions are commonly required, and hence have easy
methods to create them (via the Selector function).

  1. Those that select depending on the type of the node.
  2. Those that select depending on the attributes of the node.
  3. Those that select if a function f, returns True on the node.

Selectors can also be combined. We choose styles similar to the CSS3
combinators (http://www.w3.org/TR/css3-selectors/#combinators):

  1. And(s1, s2) returns a new selector that selects a node only if BOTH
     s1, and s2 select the node.

  2. Or(s1, s2) returns a new selector that selects a node if EITHER s1 or s2
     select the node.

  3. HasChild(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node
        * s2 selects a child of the node.

  4. HasDescendant(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node
        * s2 selects some descendant of the node.

  5. HasParent(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects the parent of the node, n.parent.

  6. HasAncestor(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects some ancestor of the node, n.


Selectors are evaluted by calling RunSelector with the selector and the
tree.

Note that combining selectors is rather inefficient right now. This will be
fixed in the future.
"""

from __future__ import absolute_import
import redhawk.utils.util as U
from . import traverse


def RunSelector(s, trees):
  """ Runs a selector, `s`, on a list of trees, `trees`, (or a single tree,
  after converting it to a list) traversing it via DFS."""
  if type(trees) is not list:
    trees = [trees]
  for tree in trees:
    for node in traverse.DFS(tree):
      if s(node):
        yield node
  return


def Selector(node_type = None
            ,function = None
            ,attr_matcher = None
            ,match_only_common_attributes = True
            ,**attrs):
  """ Return a selector function that selects based on the criteria passed.
  
  * node_type takes a string, or a class, and checks if the node type matches.
  * function takes a boolean function, and selects if function(node) is true.
  * attrs is used to match the attributes of the node at hand.

  If match_only_common_attributes is True, we match only the common attributes
  passed in, and it is considered a failure only when some attribute does not
  match, or there are no common attributes. If false, we match all attributes,
  and the absence of an attribute would mean failure.
  
  In case a function, f, is passed and match_only_common_attributes is True,
  we simply do not match a node when an AttributeError is thrown when f is
  applied on the node. If match_only_common_attributes is False, we raise the
  AttributeError, and the program is expected to handle it (or comes to a
  grinding halt!)

  If `attr_matcher` is passed, a call to attr_matcher(node_attribute,
  argument) is used to check for equality between the attribute value passed
  in, and the attribute value in the node.

  If more than one criteria is passed, all the criteria have to be satisfied for
  a node to be selected."""

  def MatchNodes(node):
    # Node Type
    if node_type:
      if type(node_type) is str:
        match = node_type == node.GetName()
      else:
        match = isinstance(node, node_type)
    else:
      match = True

    if not match: return False


    # Function
    try:
      match = function == None or function(node)
    except AttributeError as e:
      match = False 
      if not match_only_common_attributes:
        raise AttributeError(e)
        
    
    if not match: return False


    # Attribute Matching
    if not attrs: return True

    count = 0
    for (key, val) in attrs.items():
      if match_only_common_attributes is False and hasattr(node, key) is False:
        return False

      if hasattr(node, key): 
        count = 1
        if attr_matcher:
          if not attr_matcher(getattr(node, key), val):
            return False
        elif val != getattr(node, key):
          return False

    return (count != 0)

  return MatchNodes


def And(s1, s2):
  """ And(s1, s2) returns a new selector that selects a node only if BOTH
     s1, and s2 select the node."""
  return lambda x: s1(x) and s2(x)


def Or(s1, s2):
  """ Or(s1, s2) returns a new selector that selects a node if EITHER s1 or s2
     select the node."""
  return lambda x: s1(x) or s2(x)


def HasChild(s1, s2):
  """ HasChild(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node
        * s2 selects a child of the node."""
  def MatchNode(x):
    if not s1(x):
      return False

    for child in x.GetFlattenedChildren():
      if s2(child):
        return True
    return False
  return MatchNode


def HasDescendant(s1, s2):
  """ HasDescendant(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node
        * s2 selects some descendant of the node."""
  def MatchNode(x):
    if not s1(x):
      return False

    dfs = traverse.DFS(x)
    next(dfs) # Skip the current node
    for node in dfs:
      if s2(node):
        return True
    return False
  return MatchNode


def HasParent(s1, s2):
  """ HasParent(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects the parent of the node, n.parent."""
  def MatchNode(x):
    if not s1(x):
      return False

    n = x.GetParent()

    if n is not None:
      return s2(n)

  return MatchNode


def HasAncestor(s1, s2):
  """" HasAncestor(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects some ancestor of the node, n."""
  def MatchNode(x):
    if not s1(x):
      return False

    while x is not None:
      x = x.GetParent()

      if x and s2(x):
        return True

    return False
  return MatchNode
