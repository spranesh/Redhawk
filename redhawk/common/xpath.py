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

import re
from redhawk.utils.parser_combinator import (Literal, Regex, 
    Finished, Maybe, OnePlus, Choice, Sequence, Clean)

class Query:
  def ToStr(self): return ''
  def __repr__(self):
    s = self.ToStr()
    if s:
      return "%s->%s"%(self.__class__.__name__, s)
    return self.__class__.__name__

  def __str__(self): return self.__repr__()

class DotQuery(Query):
  pass

class DotDotQuery(Query):
  pass

class StarQuery(Query):
  pass

class StarStarQuery(Query):
  pass

class NodeMatchQuery(Query):
  def __init__(self, node_type, attributes, codegroup, position): 
    self.node_type = node_type
    self.attributes = dict(attributes)
    self.codegroup = codegroup
    self.position = position

    self.function = None
    if self.codegroup:
      try:
        self.function = eval('lambda n: '+ self.codegroup, {}, {})
      except StandardError, e:
        raise SyntaxError(str(e) + ": " + self.codegroup)
    return

  def ToStr(self):
    return "node_type = %s, attributes = %s, codegroup = %s, position = %s"%(
        self.node_type , self.attributes, self.codegroup, self.position)

class ChildNodeMatchQuery(Query):
  def __init__(self, q):
    self.child_query = q

  def ToStr(self): return "Child: " + self.child_query.ToStr()


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

string_parser = Clean(Regex(reg_string), lambda x: x[1:-1])
codeblock_parser = Clean(Regex(reg_codeblock), CleanAndWarnEmptyCodeBlock)
identifier_parser = Regex(reg_identifier)
number_parser = Clean(Regex(reg_number), lambda x: int(x))

attr_match_parser = Clean(
  Sequence(
    (Literal("@["), None),
    (identifier_parser, "Identifier expected"),
    (Literal("="), "'=' expected"),
    (string_parser, "String expected"),
    (Literal("]"), "Closing ']' expected")),
  lambda x: (x[1], x[3]))

position_parser = Clean(
    Sequence(
      (Literal("["), None),
      (number_parser, "Number expected"),
      (Literal("]"), "Closing ']' expected")
      ),
    lambda x: x[1])


def CleanAndWarnEmptyNodeQuery(li):
  assert(len(li) == 4)
  for x in li:
    if x:
      return NodeMatchQuery(*li)
  raise SyntaxError("Invalid or Empty NodeQuery!")

node_query_parser = Clean(
  Sequence(
    (Maybe(identifier_parser), None),
    (Maybe(OnePlus(attr_match_parser)), None),
    (Maybe(codeblock_parser), None),
    (Maybe(position_parser), None)),
  CleanAndWarnEmptyNodeQuery)

dot_parser = Clean(Literal("."), lambda x: DotQuery())
dotdot_parser = Clean(Literal(".."), lambda x: DotDotQuery())
star_parser = Clean(Literal("*"), lambda x: StarQuery())
starstar_parser = Clean(Literal("**"), lambda x: StarStarQuery())

location_query_parser = Choice(
    dotdot_parser,
    starstar_parser,
    dot_parser,
    star_parser,
    node_query_parser)

child_node_match_parser = Clean(
  Sequence(
    (Literal("["), None),
    (node_query_parser, "Expected a node query"),
    (Literal("]"), "Expected closing ']'")),
  lambda x: ChildNodeMatchQuery(x[1]))

atomic_query_parser = Choice(
    child_node_match_parser,
    location_query_parser)

slash_sep_atomic_queries_parser = OnePlus(
  Clean(
    Sequence(
        (Literal("/"), None),
        (atomic_query_parser, "Invalid Atomic Query.")),
    lambda x: x[1]))
      
xpath_query_parser = Clean(
  Sequence(
    (atomic_query_parser, "Invalid Atomic Query"),
    (Maybe(slash_sep_atomic_queries_parser, lambda: list()), None),
    (Finished(), "Left over munchies! Or maybe too few. Who's to know?")),
  lambda x: [x[0]] + x[1])

def ParseXPath(s):
  if s[0] == '/':
    raise SyntaxError("Queries should not start with a '/'")
  if s[-1] == '/':
    raise SyntaxError("Queries should not end with a '/'")
  return xpath_query_parser(s)[0]


if __name__ == '__main__':
  import sys
  print ParseXPath(sys.argv[1])
