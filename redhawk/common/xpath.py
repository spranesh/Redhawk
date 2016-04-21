#!/usr/bin/env python

""" An xpath like query system.

Inspired from: http://effbot.org/zone/element-xpath.htm

Syntax
======
Syntax: node type::  'DefineFunction'

  Selects all CHILD elements of the given node type. For example,
  'DefineFunction/FunctionArguments' selects all 'FunctionArguments' below a
  'DefineFunction' (in turn directly below the Module level).

Syntax: *

  Selects all CHILD elements. For example '*/DefineVariable' selects all
  'DefineVariable' grandchildren in the L-AST.

Syntax: **

  Selects all DESCENDANT elements. For example '**/DefineVariable' finds all
  'DefineVariable's in the L-AST.

Syntax: .
  Selects the CURRENT element. This is mostly useful just to indicate that the
  path is a relative one.

Syntax: ..
  Selects the parent element. For example, 'A/B/..' would select all 'A'
  which have 'B' as a child.

Syntax: DefineVariable@[name1='value1']@[name2='value2']@{n.foo == 'blah'}[2]
  Selects CHILD elements which match the node type 'DefineVariable', has
  attribute name1, which has a value of 'value1', and an attribute name2,
  which has a value of 'value2'. Furthermore it satifies the codeblock with n
  as the child node. That is,
    (lambda n: n.foo == 'blah')(child_node)
  is True. Among the list of all such children, it selects the 3rd child
  (index 2).

  Each of the node type, attribute value pairs, codegroup, and index is
  optional as can be seen in the grammar below. The above syntax is called a
  NodeQuery syntax.

Syntax: (NodeQuery)
  Return all nodes whose CHILD nodes satisfy NodeQuery. This is equivalent to
  /NodeQuery/..


Examples
========
Select all Functions one level below module level:

  'DefineFunction'

Select all methods:

  '**/DefineClass/DefineFunction'

Select all Closures (Funcdef within a Funcdef):

  '**/DefineFunction/**/DefineFunction'


Position Syntax
---------------

The position in a Node Query is a comma separated list of numbers.

  1. The position given indicates the position of the given node, among it's
     parents children. They are ZERO-indexed, and can be negative.

  2. If only one position is given, i.e, the position list is of the form [i],
     then the children of that node will be flattened out, and the ith child will
     be returned.

  3. The zero index is special. Any node returned by [2, 1] will be returned
     by [2, 1, 0] and [2, 1, 0, 0] and so forth. Note that [2, 0, 0] may be
     different from [2, 0].

     In other words, the 0 index, in a mutli-index query succeeds even if it
     is a list or not.

  4. If more than one position list is given, then the children will be
     traversed in the order of the positions given.

Examples:

Select all second arguments to a function:
  '**/DefineFunction/FunctionArguments/[1]'

Select all fifth arguments to a function:
  '**/DefineFunction/FunctionArguments/[4]'

Select all first keyword arguments to a function. Keyword Arguments is the
3rd child in a FunctionArguments node, as can be seen in _node_cfg.yaml. This
succeeds even though keyword arguments is not a list, because of the
zero-index speciality.

  '**/DefineFunction/FunctionArguments/[2, 0]'


Grammar
=======

XPathQuery = AtomicQuery ('/' AtomicQuery)*

AtomicQuery = LocationQuery
            | (LocationQuery)     # ChildNodeMatchQuery query

LocationQuery =   .
                | ..
                | *
                | **
                | NodeQuery


NodeQuery = identifier? @[identifier=string]* @{codeblock}? Position*

Position = [ comma-separated-list-of-numbers ]
"""
from __future__ import absolute_import
from __future__ import print_function
from . import _selector
from . import traverse

import redhawk.utils.parser_combinator as P
import redhawk.utils.util as U

import itertools
import re
import sys

from six.moves import filter

# All our filter functions are from sequences to sequences
#   Filter :: Iterable -> Iterable

def Children(it):
  """ Return a generator to the children of all the nodes in the passed
  iterable."""
  for n in it:
    for c in n.GetFlattenedChildren():
      if c is not None:
        yield c

def Parents(it):
  """ Return a generator to the parents of all the nodes in the passed
  iterable. Note that we first use a set to remove duplicates among the
  parents."""
  return iter(set((n.GetParent() for n in it if n.GetParent() != None)))


class Query:
  def ToStr(self): return ''

  def Filter(self):
    raise NotImplementedError("Not Implemented in base class!")

  def __repr__(self):
    s = self.ToStr()
    if s: return "%s->%s"%(self.__class__.__name__, s)
    return self.__class__.__name__

  def __str__(self):
    return self.__repr__()


class DotQuery(Query):
  def Filter(self, it):
    return it


class DotDotQuery(Query):
  def Filter(self, it):
    return Parents(it)


class StarQuery(Query):
  def Filter(self, it):
    return Children(it)

class StarStarQuery(Query):
  """Match everything excluding the current node."""
  def Filter(self, it):
    """ We do not want duplicates. This means storing all the objects into a
    set. This is an expensive operation in memory, and in time O(n log n). We
    just skip this for now, but probably need to come up with (heuristic
    ways?) later."""
    iterators = (traverse.DFS(i) for i in it)
    return itertools.chain(*iterators)


class NodeMatchQuery(Query):
  """ Select child elements that match."""
  # By default variables are '', if not found
  def __init__(self, node_type, attributes, codegroup, position_list):
    self.node_type = node_type or None
    self.attributes = dict(attributes)
    self.codegroup = codegroup or None
    self.position_list = position_list or None

    # Try creating to only warn of errors.
    self.__CreateFunctionFromCodeGroup()
    return

  def __CreateFunctionFromCodeGroup(self):
    if self.codegroup:
      try:
        return eval('lambda n: '+ self.codegroup, {}, {})
      except Exception as e:
        raise SyntaxError(str(e) + ": " + self.codegroup)
    return None


  def Filter(self, it):
    # Create lambda at runtime so that an object of the class
    # can be pickled - a parsed query is stuff we send to multiple processes
    # in  parallel python.
    it = Children(it)
    s = _selector.Selector(
        node_type = self.node_type,
        function = self.__CreateFunctionFromCodeGroup(),
        **self.attributes)
    matched_nodes = filter(s, it)

    if not self.position_list:
      return matched_nodes

    return self.__GetNodesInPosition(matched_nodes)

  def __GetNodesInPosition(self, matched_nodes):
    for n in matched_nodes:
      parents = n.GetParent()
      if parents is None:
        continue

      if len(self.position_list) == 1:
        children = parents.GetFlattenedChildren()
      else:
        children = parents.GetChildren()

      indexed_node = U.IndexInto(children, self.position_list)
      if indexed_node == n:
        yield n


  def ToStr(self):
    return "node_type = %s, attributes = %s, codegroup = %s, position_list = %s"%(
        self.node_type , self.attributes, self.codegroup, self.position_list)


class ChildNodeMatchQuery(Query):
  """ Select nodes whose child element matches the given query."""
  def __init__(self, q):
    assert(isinstance(q, NodeMatchQuery))
    self.child_query = q

  def ToStr(self): return "Child: " + self.child_query.ToStr()

  def Filter(self, it):
    filtered_children = self.child_query.Filter(it)
    return Parents(filtered_children)

# Parse xpath
reg_identifier = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
reg_string     = re.compile(r"'[^']*'|" + r'"[^"]*"')
reg_codeblock  = re.compile(r"@{[^}]*}")
reg_number     = re.compile(r"-?[0-9]+")
reg_position   = re.compile(r"[0-9,\- ]+")

# Warn people of Empty Codeblocks
def CleanAndWarnEmptyCodeBlock(s):
  r = s[2:-1]
  if not r: raise SyntaxError("Empty Code block found.")
  return r

def CleanPosition(s):
  numbers = []
  for n in s.split(","):
    try:
      numbers.append(int(n))
    except ValueError as e:
      raise SyntaxError("Unable to parse '%s' into a number in position syntax : '%s'"
          %(n, s))
  return numbers

string_parser = P.Clean(P.Regex(reg_string), lambda x: x[1:-1])
codeblock_parser = P.Clean(P.Regex(reg_codeblock), CleanAndWarnEmptyCodeBlock)
identifier_parser = P.Regex(reg_identifier)
number_parser = P.Clean(P.Regex(reg_number), lambda x: int(x))
position_parser = P.Clean(P.Regex(reg_position), CleanPosition)

attr_match_parser = P.Clean(
  P.Sequence(
    (P.Literal("@["), None),
    (identifier_parser, "Identifier expected"),
    (P.Literal("="), "'=' expected"),
    (string_parser, "String expected"),
    (P.Literal("]"), "Closing ']' expected")),
  lambda x: (x[1], x[3]))

position_parser = P.Clean(
    P.Sequence(
      (P.Literal("["), None),
      (position_parser, "expected a position: comma-separated-list-of-numbers. "),
      (P.Literal("]"), "Closing ']' expected")
      ),
    lambda x: x[1])


def CleanAndWarnEmptyNodeQuery(li):
  assert(len(li) == 4)
  for x in li:
    if x:
      return NodeMatchQuery(*li)
  raise SyntaxError("Invalid or Empty NodeQuery!")

node_query_parser = P.Clean(
  P.Sequence(
    (P.Maybe(identifier_parser), None),
    (P.Maybe(P.OnePlus(attr_match_parser)), None),
    (P.Maybe(codeblock_parser), None),
    (P.Maybe(position_parser), None)),
  CleanAndWarnEmptyNodeQuery)

dot_parser = P.Clean(P.Literal("."), lambda x: DotQuery())
dotdot_parser = P.Clean(P.Literal(".."), lambda x: DotDotQuery())
star_parser = P.Clean(P.Literal("*"), lambda x: StarQuery())
starstar_parser = P.Clean(P.Literal("**"), lambda x: StarStarQuery())

location_query_parser = P.Choice(
    dotdot_parser,
    starstar_parser,
    dot_parser,
    star_parser,
    node_query_parser)

child_node_match_parser = P.Clean(
  P.Sequence(
    (P.Literal("("), None),
    (node_query_parser, "Expected a node query"),
    (P.Literal(")"), "Expected closing ')'")),
  lambda x: ChildNodeMatchQuery(x[1]))

atomic_query_parser = P.Choice(
    child_node_match_parser,
    location_query_parser)

slash_sep_atomic_queries_parser = P.OnePlus(
  P.Clean(
    P.Sequence(
        (P.Literal("/"), None),
        (atomic_query_parser, "Invalid Atomic Query.")),
    lambda x: x[1]))

xpath_query_parser = P.Clean(
  P.Sequence(
    (atomic_query_parser, "Invalid Atomic Query"),
    (P.Maybe(slash_sep_atomic_queries_parser, lambda: list()), None),
    (P.Finished(), "Left over munchies! Or maybe too few. Who's to know?")),
  lambda x: [x[0]] + x[1])


def ApplyParsedXPathQuery(trees, xpath_query):
  """ Apply a parsed XPath Query to a list (sequence) of `trees`."""
  filtered_nodes = iter(trees[:])

  for q in xpath_query:
    filtered_nodes = q.Filter(filtered_nodes)

  return filtered_nodes


def ParseXPath(s):
  """ Parse an XPath Query."""
  if s[0] == '/':
    raise SyntaxError("Queries should not start with a '/'")
  if s[-1] == '/':
    raise SyntaxError("Queries should not end with a '/'")
  try:
    return xpath_query_parser(s)[0]
  except SyntaxError as e:
    print("Syntax Error: %s"%(e))
    sys.exit(1)
  return


def XPath(trees, xpath_string):
  """ Parse and apply the xpath query in `xpath_string` to the list (sequence)
  of `trees`."""
  return ApplyParsedXPathQuery(trees, ParseXPath(xpath_string))


def Main():
  """ Only for testing."""

  from . import format_position as F
  import redhawk.common.get_ast as G

  if len(sys.argv) < 2:
    print(""" %s <xpath-query> [files].

    If files are not given, the parsed xpath-query is printed.
    Otherwise the concerned lines in each file is printed."""%(sys.argv[0]))
    sys.exit(1)

  parsed_query = ParseXPath(sys.argv[1])
  if len(sys.argv) == 2:
    print(parsed_query)
    return

  for f in sys.argv[2:]:
    ast = G.GetLAST(f, database = None)
    results = list(ApplyParsedXPathQuery([ast], parsed_query))
    for r in results:
      F.PrintContextInFile(r,context=3)
  return

if __name__ == '__main__':
  Main()
