#!/usr/bin/env python

""" Test XPath."""

import xpath as X

import nose.tools

def RaisesSyntaxError(delayed_callable):
  assert(callable(delayed_callable))
  raises = False
  try:
    delayed_callable()
  except SyntaxError, e:
    raises = True

  assert raises, "Expression Does not Raise Syntax Error"


def TestStringParser():
  assert(X.string_parser("'foobar'") == ("foobar", ""))
  assert(X.string_parser('"foobar"') == ("foobar", ""))

def TestIdentifierParser():
  assert(X.identifier_parser("foobar") == ("foobar", ""))
  assert(X.identifier_parser("@foobar") == (None, "@foobar"))
  assert(X.identifier_parser("9foobar") == (None, "9foobar"))
  assert(X.identifier_parser("_foobar9") == ("_foobar9", ""))

def TestCodeBlockParser():
  assert(X.codeblock_parser("@{foo bar}") == ("foo bar", ""))
  assert(X.codeblock_parser("@{foo bar}fg") == ("foo bar", "fg"))

@nose.tools.raises(SyntaxError)
def TestCodeBlockParserFailure():
  X.codeblock_parser("@{}")

def TestNumberParser():
  assert(X.number_parser("1231") == (1231, ""))
  assert(X.number_parser("1231fg") == (1231, "fg"))
  return

def TestPositionParser():
  assert(X.position_parser("[1231]") == (1231, ""))
  assert(X.position_parser("[1231]fg") == (1231, "fg"))

  # Test Syntax Errors thrown up
  e1, e2 = False, False

  RaisesSyntaxError(lambda: X.position_parser("["))
  RaisesSyntaxError(lambda: X.position_parser("[1231"))


def TestAttrMatchParser():
  assert(X.attr_match_parser("@[foo='blah']") == (("foo", "blah"), ""))
  assert(X.attr_match_parser("@[foo='blah']f") == (("foo", "blah"), "f"))

  RaisesSyntaxError(lambda: X.attr_match_parser("@["))
  RaisesSyntaxError(lambda: X.attr_match_parser("@[foo"))
  RaisesSyntaxError(lambda: X.attr_match_parser("@[foo="))
  RaisesSyntaxError(lambda: X.attr_match_parser("@[foo='blah'"))
  RaisesSyntaxError(lambda: X.attr_match_parser("@[foo "))
  RaisesSyntaxError(lambda: X.attr_match_parser("@[foo= "))

def TestNodeQueryParser():
  assert(isinstance(
    X.node_query_parser("DefineVariable")[0],
    X.NodeMatchQuery))

  assert(isinstance(
    X.node_query_parser(
      "ForEach@[foo='blah']@{codegroup}[12]")[0],
    X.NodeMatchQuery))


def TestChildNodeMatchParser():
  assert(isinstance(
    X.child_node_match_parser("[DefineVariable]")[0],
    X.ChildNodeMatchQuery))

  assert(isinstance(
    X.child_node_match_parser(
      "[ForEach@[foo='blah']@{codegroup}[12]]")[0],
    X.ChildNodeMatchQuery))

  RaisesSyntaxError(lambda: X.child_node_match_parser(
    "[..]"))

  RaisesSyntaxError(lambda: X.child_node_match_parser(
    "[.]"))

  RaisesSyntaxError(lambda: X.child_node_match_parser(
    "[**]"))

def TestAtomicQueryParser():
  # Test this function rather thoroughly
  assert(isinstance(
    X.atomic_query_parser(".")[0],
    X.DotQuery))

  assert(isinstance(
    X.atomic_query_parser("..")[0],
    X.DotDotQuery))

  assert(isinstance(
    X.atomic_query_parser("*")[0],
    X.StarQuery))

  assert(isinstance(
    X.atomic_query_parser("**")[0],
    X.StarStarQuery))

  assert(isinstance(
    X.child_node_match_parser(
      "[ForEach@[foo='blah']@{codegroup}[12]]")[0],
    X.ChildNodeMatchQuery))

  assert(isinstance(
    X.node_query_parser(
      "ForEach@[foo='blah']@{codegroup}[12]")[0],
    X.NodeMatchQuery))

  assert(isinstance(
    X.node_query_parser(
      "ForEach@{codegroup}[12]")[0],
    X.NodeMatchQuery))

def TestSlashSepAtomicQueriesParser():
  result = X.slash_sep_atomic_queries_parser(
      "/./../*/**/[DefineVariable]/@[foo='blah']")[0]
  assert(isinstance(result[0], X.DotQuery))
  assert(isinstance(result[1], X.DotDotQuery))
  assert(isinstance(result[2], X.StarQuery))
  assert(isinstance(result[3], X.StarStarQuery))
  assert(isinstance(result[4], X.ChildNodeMatchQuery))
  assert(isinstance(result[5], X.NodeMatchQuery))

  RaisesSyntaxError(lambda: X.slash_sep_atomic_queries_parser(
    "/../"))


def TestParseXPath():
  # Thoroughly test final function
  query = ("./../*/**/[DefineVariable]/@[foo='blah']"
          + "/@{n.blah == None}/@{n.blah == None}")
  # No leading or trailing slash
  RaisesSyntaxError(lambda: X.ParseXPath(query + "/"))
  RaisesSyntaxError(lambda: X.ParseXPath("/" + query))

  _, leftover = X.xpath_query_parser(query)
  assert(leftover == "")

  result = X.ParseXPath(query)

  assert(isinstance(result[0], X.DotQuery))
  assert(isinstance(result[1], X.DotDotQuery))
  assert(isinstance(result[2], X.StarQuery))
  assert(isinstance(result[3], X.StarStarQuery))
  assert(isinstance(result[4], X.ChildNodeMatchQuery))
  assert(isinstance(result[5], X.NodeMatchQuery))
  assert(isinstance(result[6], X.NodeMatchQuery))
  assert(isinstance(result[7], X.NodeMatchQuery))
  return

