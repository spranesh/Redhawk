#!/usr/bin/env python

""" A selector is a function that operates on a node, and decides if it should
be selected. Selectors can be combined using the Combine Function, and also
composed (in a monadic function) using the Compose Function below.

We have helper functions for creating two types of selectors:

    NodeSelector: A Selector that selects a particular type of node.

    AttributeSelector: A Selector that selects a node when its attribtues have
    certain values.
"""

import redhawk.utils.util as U
import walk

def Select(tree, selector):
  """ A generator that returns nodes, `n`, in the tree, `tree`
  for which `selector(n)` is True.
  
  Select :: tree -> selector -> [tree]"""
  for n in walk.Walk(tree):
    if selector(n):
      yield n

def Combine(*selectors):
  """ Combines selectors s1, s2, .. , so that the resultant selector
  returns True iff s1 returns True, s2 returns True, ..."""
  return lambda n: all([s(n) for s in selectors])


def Compose(tree, selector1, selector2):
  """ A composition combinator (similar to Haskell's list monad bind) for the
  output of the select function.

  This is equivalent to 
    Concat(map(selector2, Select(tree, selector1)))
    
  Combine :: tree -> selector -> selector -> [tree] """

  return U.Concat(map(selector2, Select(tree, selector1)))


def NodeSelector(t):
  """ Return a Selector that selects nodes of type t.
  
  Either a string or a type can be passed in. Strings are matched with
  GetName(), and types are matched with type(node)."""
  if type(t) == str:
    return lambda n: n.GetName() == t
  elif type(t) == type:
    return lambda n: type(n) == t

  # Otherwise exit with error
  U.ExitWithError("selector.NodeSelector: Passed in argument is of unknown \
  type : %s"%(type(n)))


def AttributeSelector(match_all_attributes = True, **attrs):
  """ Returns a selector which returns True, when all the arguments passed in
  match the attributes of the node being considered.

  If the match_all_attributes option is False, then we only care to
  match the common options (note that there can be None, in which case the
  selector returns True).

  If match_all_attributes is True, we match all the options passed
  in, and it is considered a failure when any required attribute either
  differs, or is not present in the node.

  (match_all_attributes is set to True by default).
  """
  def MatchesAttributes(n):
    for a in attrs:
      if hasattr(n, a):
        if getattr(n, a) != attrs[a]:
          return False

      elif match_all_attributes:
        return False

    return True
  return MatchesAttributes

