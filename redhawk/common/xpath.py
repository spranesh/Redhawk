#!/usr/bin/env python

""" An xpath like query system.


XPathQuery = AtomicQuery ('/' AtomicQuery)*

AtomicQuery = LocationQuery
            | [LocationQuery]     # ChildNodeMatchQuery query

LocationQuery =   .
                | ..
                | *
                | **
                | NodeQuery


NodeQuery = identifier? @[identifier=string]* @{codeblock}? [number]

"""
import _selector
import traverse

import redhawk.utils.parser_combinator as P
import redhawk.utils.util as U

import itertools
import re
import sys

# All our filter functions are from sequences to sequences
#   Filter :: Iterable -> Iterable

def Children(it):
  """ Return a generator to the children of all the nodes in the passed
  iterable."""
  for n in it:
    for c in U.Flatten(n.GetChildren()):
      if c is not None:
        yield c

def Parents(it):
  """ Return a generator to the parents of all the nodes in the passed
  iterable. Note that we first use a set to remove duplicates among the
  parents."""
  return iter(set((n.GetParent() for n in it)))


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
  def Filter(self, it):
    """ We do not want duplicates. This means storing all the objects into a
    set. This is an expensive operation in memory, and in time O(n log n). We
    are doing this for now, but probably need to come up with (heuristic
    ways?) later."""
    iterators = [traverse.DFS(i) for i in it]
    return iter(set(itertools.chain(*iterators)))


class NodeMatchQuery(Query):
  # By default variables are '', if not found
  def __init__(self, node_type, attributes, codegroup, position):
    self.node_type = node_type or None
    self.attributes = dict(attributes)
    self.codegroup = codegroup or None
    self.position = position or None

    self.function = None
    if self.codegroup:
      try:
        self.function = eval('lambda n: '+ self.codegroup, {}, {})
      except StandardError, e:
        raise SyntaxError(str(e) + ": " + self.codegroup)
    return

  def Filter(self, it):
    it = Children(it) # The children of the given nodes are checked.
    s = _selector.Selector(node_type = self.node_type,
                           function = self.function,
                           **self.attributes)
    matched_nodes = itertools.ifilter(s, it)
    if self.position is not None:
      matched_nodes = list(matched_nodes)
      if self.position < len(matched_nodes):
        return iter([matched_nodes[self.position]])
      else:
        return iter([])
    return matched_nodes

  def ToStr(self):
    return "node_type = %s, attributes = %s, codegroup = %s, position = %s"%(
        self.node_type , self.attributes, self.codegroup, self.position)


class ChildNodeMatchQuery(Query):
  def __init__(self, q):
    assert(isinstance(q, NodeMatchQuery))
    self.child_query = q

  def ToStr(self): return "Child: " + self.child_query.ToStr()

  def Filter(self, it):
    # Query the children. Since child_query is a NodeMatchQuery, it
    # automatically checks the children.
    filtered_children = self.child_query.Filter(it)
    parents_of_filtered_children = Parents(filtered_children)
    return parents_of_filtered_children

# Parse xpath
reg_identifier = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
reg_string     = re.compile(r"'[^']*'|" + r'"[^"]*"')
reg_codeblock  = re.compile(r"@{[^}]*}")
reg_number     = re.compile(r"-?[0-9]+")

# Warn people of Empty Codeblocks
def CleanAndWarnEmptyCodeBlock(s):
  r = s[2:-1]
  if not r: raise SyntaxError("Empty Code block found.")
  return r

string_parser = P.Clean(P.Regex(reg_string), lambda x: x[1:-1])
codeblock_parser = P.Clean(P.Regex(reg_codeblock), CleanAndWarnEmptyCodeBlock)
identifier_parser = P.Regex(reg_identifier)
number_parser = P.Clean(P.Regex(reg_number), lambda x: int(x))

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
      (number_parser, "Number expected"),
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
    (P.Literal("["), None),
    (node_query_parser, "Expected a node query"),
    (P.Literal("]"), "Expected closing ']'")),
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

def ParseXPath(s):
  """ Parse an XPath Query."""
  if s[0] == '/':
    raise SyntaxError("Queries should not start with a '/'")
  if s[-1] == '/':
    raise SyntaxError("Queries should not end with a '/'")
  try:
    return xpath_query_parser(s)[0]
  except SyntaxError, e:
    print "Syntax Error: %s"%(e)
    sys.exit(1)
  return

def ApplyParsedXPathQuery(trees, xpath_query):
  """ Apply a parsed XPath Query to a list (sequence) of `trees`."""
  assert(type(xpath_query) == list)
  filtered_nodes = iter(trees[:])
  for q in xpath_query:
    filtered_nodes = q.Filter(filtered_nodes)
  return list(filtered_nodes)

def XPath(trees, xpath_string):
  """ Parse and apply the xpath query in `xpath_string` to the list (sequence)
  of `trees`."""
  return ApplyParsedXPathQuery(trees, ParseXPath(xpath_string))


def Main():
  """ Only for testing."""

  import position
  import redhawk.utils.get_ast as G

  if len(sys.argv) < 2:
    print """ %s <xpath-query> [files].

    If files are not given, the parsed xpath-query is printed.
    Otherwise the concerned lines in each file is printed."""%(sys.argv[0])
    sys.exit(1)

  parsed_query = ParseXPath(sys.argv[1])
  if len(sys.argv) == 2:
    print parsed_query
    return

  for f in sys.argv[2:]:
    ast = G.GetLAST(f, database = None)
    results = list(ApplyParsedXPathQuery([ast], parsed_query))
    print "+++ %s"%(f)
    for r in results:
      print position.ShowPosition(position.GetPosition(r))
    print
  return

if __name__ == '__main__':
  Main()
