#!/usr/bin/env python

""" A selector is a function that selects some nodes of the AST depending on
some constraints. Selector functions have the type

    selector :: tree -> Bool

Three types of selector functions are commonly required, and hence have easy
methods to create them (via the Selector (S) function).

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

  4. HasDescendent(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node
        * s2 selects some descendant of the node.

  5. HasParent(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects the parent of the node, n.parent.

  6. HasAncestor(s1, s2) returns a selector that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects some ancestor of the node, n.


Selectors are evaluted by calling RunSelector (R) with the selector and the
tree.

Note that combining selectors is rather inefficient right now. This will be
fixed in the future.
"""

import redhawk.utils.util as U
import traverse


def RunSelector(s, tree):
  """ Runs a selector, `s`, on a tree, `tree`, traversing it via DFS."""
  for node in traverse.DFS(tree):
    if s(node):
      yield node
  return


def Selector(node_type = None
            ,function = None
            ,match_only_common_attributes = False
            ,**attrs):
  """ Return a selector function that selects based on the criteria passed.
  
  * node_type accepts a string, or a class, and checks if the node type matches.
  * function accepts a boolean function, and selects if function(node) is true.
  * attrs is used to match the attributes of the node at hand.

  If match_only_common_attributes is True, we match only the common attributes
  passed in, and it is considered a failure only when some attribute does not
  match, or there are no common attributes.

  If more than one criteria is passed, all the criteria have to be satisfied for
  a node to be selected."""

  def MatchNodes(node):
    match = (node_type == None
            or node_type == node.GetName()
            or node_type == type(node))

    if not match: return False

    match = function == None or function(node)
    
    if not match: return False

    if not attrs: return True

    count = 0
    for (key, val) in attrs.items():
      if match_only_common_attributes is False and hasattr(node, key) is False:
        return False

      if hasattr(node, key): 
        count = 1
        if val != getattr(node, key):
          return False

    return (count != 0)

  return MatchNodes

# For shorthand
S = Selector    
R = RunSelector 

