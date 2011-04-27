#!/usr/bin/env python

""" A selector is a function that selects some nodes of the AST depending on
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

The `S` class can also be used to create and combine selectors. This is the
method currently recommended.

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
            ,attr_matcher = None
            ,match_only_common_attributes = False
            ,**attrs):
  """ Return a selector function that selects based on the criteria passed.
  
  * node_type takes a string, or a class, and checks if the node type matches.
  * function takes a boolean function, and selects if function(node) is true.
  * attrs is used to match the attributes of the node at hand.

  If match_only_common_attributes is True, we match only the common attributes
  passed in, and it is considered a failure only when some attribute does not
  match, or there are no common attributes.

  If `attr_matcher` is passed, a call to attr_matcher(node_attribute,
  argument) is used to check for equality between the attribute value passed
  in, and the attribute value in the node.

  If more than one criteria is passed, all the criteria have to be satisfied for
  a node to be selected."""

  def MatchNodes(node):
    if node_type:
      if type(node_type) is str:
        match = node_type == node.GetName()
      else:
        match = isinstance(node, node_type)
    else:
      match = True

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

    for child in U.Flatten(x.GetChildren()):
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

    for node in traverse.DFS(x):
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



# Shorthand use of the selector API.
class S:
  """ If this shorthand API is used, it must be used consistently. All
  arguments must be objects of this class.

  """

  def __init__(self
              ,selector_function = None
              ,node_type = None
              ,function = None
              ,attr_matcher = None
              ,match_only_common_attributes = False
              ,**attrs):
    """ Create a selector object.

    * selector_function, if not None, indicates that the function being passed
      in is already a selector (created using the Selector function). All other
      parameters are ignored.

    * node_type takes a string, or a class, and checks if the node type matches.
    * function takes a boolean function, and selects if function(node) is true.
    * attrs is used to match the attributes of the node at hand.
    
    For more help, see the Selector function in this module."""

    if selector_function:
      self.selector = selector_function
    else:
      self.selector = Selector(node_type = node_type
                              ,function = function
                              ,attr_matcher = attr_matcher
                              ,match_only_common_attributes = match_only_common_attributes
                              **attrs)
    return


  def __lshift__(self, selector):
    """ A << B is A.HasAncestor(B)"""
    return self.HasAncestor(selector)


  def __rshift__(self, selector):
    """ A >> B is A.HasDescendant(B) """
    return self.HasDescendant(selector)


  def __call__(self, tree):
    """ Calls RunSelector on the tree with the given selector."""
    return RunSelector(self.selector, tree)


  def __GetSelectorFunction(self, selector_or_selector_object):
    """ Get the selector function from a variable which may either be a
    selector or a selector object."""
    if isinstance(selector_or_selector_object, S):
      return selector_or_selector_object.selector
    else:
      return selector_or_selector_object


  def HasChild(self, selector):
    """ Returns a NEW selector that requires the current selector be valid,
    and `selector` to be valid on one of its children.

    See the HasChild function in the module for more help."""
    return S(HasChild(self.selector
                     ,self.__GetSelectorFunction(selector)))


  def HasDescendant(self, selector):
    """ Returns a NEW selector that requires the current selector be valid,
    and the `selector` to be valid on one of its parents.

    See the HasDescendant function in the module for more help."""
    return S(HasDescendant(self.selector
                      ,self.__GetSelectorFunction(selector)))


  def HasParent(self, selector):
    """ Returns a NEW selector that requires the current selector be valid,
    and the `selector` to be valid on one of its parents.

    See the HasParent function in the module for more help."""
    return S(HasParent(self.selector
                      ,self.__GetSelectorFunction(selector)))
              

  def HasAncestor(self, selector):
    """ Returns a NEW selector that requires the current selector be valid,
    and the `selector` to be valid on one of its ancestors.

    See the HasAncestor function in the module for more help."""
    return S(HasAncestor(self.selector
                        ,self.__GetSelectorFunction(selector)))

  def And(self, selector):
    """ Returns a NEW selector that requires the current selector be valid,
    and the `selector` also to be valid.

    See the And function in the module for more help."""
    return S(And(self.selector
                ,self.__GetSelectorFunction(selector)))


  def Or(self, selector):
    """ Returns a NEW selector that requires the current selector be valid,
    or the `selector` to be valid.

    See the Or function in the module for more help."""
    return S(Or(self.selector
               ,self.__GetSelectorFunction(selector)))
