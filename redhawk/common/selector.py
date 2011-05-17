#!/usr/bin/env python

""" 
S-objects (or selector-objects) can be used to select some nodes of an AST
depending on various constraints. Three common types of selections involve:

  1. Selecting based on the type of the node.
  2. Selecting based on the attributes of the node.
  3. Selecting based on some custom criteria, i.e, whether a function f,
     returns True for the given node.

The S-Object for each of the cases can be instantiated as follows:

  >>> import redhawk.common.selector as S
  >>> s1 = S(node_type = 'DefineFunction')
  >>> s2 = S(name = 'foobar')
  >>> s3 = S(function = lambda x: len(x.GetChildren()) > 3)

Selector-objects are evaluted by calling it with a tree or list of trees. (The
__call__ method of the S-objects have been overriden).

  >>> # Get trees t1, t2, t3
  >>> s1(t1) # Select nodes in t1 which have are of type DefineFunction
  >>> s2([t1, t2, t3]) # Select nodes where an attribute name has attribute foobar.

Evaluating an s-object returns a (possibly empty) iterator to the selected
nodes.

Selector-objects objects can be combined. We chose styles similar to the CSS3
combinators (http://www.w3.org/TR/css3-selectors/#combinators):

  1. s1.And(s2) returns a NEW s-object that selects a node only if BOTH s1,
    and s2 select the node.

  2. s1.Or(s2) returns a NEW new s-object that selects a node if EITHER s1 or s2
     select the node.

  3. s1.HasChild(s2) returns a NEW s-object that selects a node, n, only if
        * s1 selects the node
        * s2 selects a child of the node.

  4. s1.HasDescendant(s2) returns a NEW s-object that selects a node, n, only if
        * s1 selects the node
        * s2 selects some descendant of the node.

  5. s1.HasParent(s2) returns a NEW s-object that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects the parent of the node, n.parent.

  6. s1.HasAncestor(s2) returns a NEW s-object that selects a node, n, only if
        * s1 selects the node, n
        * s2 selects some ancestor of the node, n.


Example:

Find all private functions (those that start with __), of all classes
that inherits from some particular class, 'Foo'
  
  >>> import selector as S
  >>> private_function = S.S(node_type = 'DefineFunction',
                             function = lambda x: x.name.name[:2] == '__')
  >>> inherited_classes = S.S(node_type = 'DefineClass',
                              function = lambda x: 'Foo' in x.inherits)
  >>> required_functions = private_function.HasParent(inherited_classes)
  >>> required_functions(tree)


(Note that the HasDescendant selector is a little inefficient right now. This
should be fixed in the future).

(See _selector.py for implementation details).
"""

import _selector

# Shorthand use of the selector API.
class S:
  def __init__(self
              ,selector_function = None
              ,node_type = None
              ,function = None
              ,attr_matcher = None
              ,match_only_common_attributes = True
              ,**attrs):
    """ Create a selector object that selects based on the criteria passed.
    
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
    a node to be selected.

    (A Selector function as described in the _selector module can also be
    passed. For more help, see the Selector function in the _selector module)."""

    if selector_function:
      self.selector = selector_function
    else:
      self.selector = _selector.Selector(
                         node_type = node_type
                        ,function = function
                        ,attr_matcher = attr_matcher
                        ,match_only_common_attributes = match_only_common_attributes,
                        **attrs)
    return


  def __lshift__(self, selector):
    """ A << B is A.HasAncestor(B)"""
    return self.HasAncestor(selector)


  def __rshift__(self, selector):
    """ A >> B is A.HasDescendant(B) """
    return self.HasDescendant(selector)


  def __call__(self, tree):
    """ Calls _selector.RunSelector on a tree (or list of trees) with the
    given selector."""
    return _selector.RunSelector(self.selector, tree)

  def Apply(self, trees):
    """ This applies the selector on a LIST of `trees`. This method returns an
    For each resulting node, n, a pair is returned:

      (n, tree in `trees` from which n was selected)

    This method, thus returns an iterator to a pair of trees.

    Example: Suppose t1 contains two nodes, n1, n2 that match some selector,
    s. And t2 contains three nodes, m1, m2, m3, that match the selector, s.

    Then s.Apply([t1, t2]) returns an *iterator* to the *set*:

      (n1, t1), (n2, t1), (m1, t2), (m2, t2), (m2, t3)

    The order of nodes is NOT guaranteed."""

    assert(type(trees) is list)
    for t in trees:
      for n in self(t):
        yield (n, t)

  def And(self, s):
    """ Returns a NEW selector that requires the current s-object be valid,
    and the `s` s-object also to be valid.

    See the And function in the module for more help."""
    return S(_selector.And(self.selector, s.selector))

  def Or(self, s):
    """ Returns a NEW selector that requires the current s-object be valid,
    or the `s` s-object to be valid.

    See the Or function in the module for more help."""
    return S(_selector.Or(self.selector, s.selector))

  def HasChild(self, s):
    """ Returns a NEW selector that requires the current s-object be valid,
    and `s` s-object to be valid on one of its children.

    See the HasChild function in the module for more help."""
    return S(_selector.HasChild(self.selector, s.selector))

  def HasDescendant(self, s):
    """ Returns a NEW selector that requires the current s-object be valid,
    and the `s` s-object to be valid on one of its parents.

    See the HasDescendant function in the module for more help."""
    return S(_selector.HasDescendant(self.selector, s.selector))

  def HasParent(self, s):
    """ Returns a NEW selector that requires the current s-object be valid,
    and the `s` s-object to be valid on one of its parents.

    See the HasParent function in the module for more help."""
    return S(_selector.HasParent(self.selector, s.selector))
              
  def HasAncestor(self, s):
    """ Returns a NEW selector that requires the current s-object be valid,
    and the `s` s-object to be valid on one of its ancestors.

    See the HasAncestor function in the module for more help."""
    return S(_selector.HasAncestor(self.selector, s.selector))
