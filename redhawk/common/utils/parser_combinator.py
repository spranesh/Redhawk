#!/usr/bin/env python

""" A simple parser combinator library.
A parser is of type Parser :: s -> (object, remaining string) """

def Literal(literal):
  def NewParser(s):
    if s[:len(literal)] == literal:
      return (literal, s[len(literal):])
    return (None, s)
  return NewParser

def Regex(regex_object):
  assert hasattr(regex_object, 'match'), "regex object was not passed" 
  def NewParser(s):
    m = regex_object.match(s)
    if m:
      return (s[m.start():m.end()], s[m.end():])
    return (None, s)
  return NewParser

def Finished():
  def NewParser(s):
    if s == "": return ('', '')
    else: return (None, s)
  return NewParser

# Parser Combinators - Maybe, Many, Choice and Sequence
# If the parser fails, make it return a ''
def Maybe(p, empty = lambda: str()): # Universal Parser
  def NewParser(s):
    (m, r) = p(s)
    if m == None: m = empty()
    return (m, r)
  return NewParser

def OnePlus(p): # Do not pass a Universal Parser here!
  def NewParser(s):
    results = []
    old, (m, s) = s, p(s)
    if m == None: return (None, old)
    while m != None:
      results.append(m)
      old, (m, s) = s, p(s)
    return (results, old)
  return NewParser

def Choice(*parsers):
  def NewParser(s):
    for p in parsers:
      (m, r) = p(s)
      if m: return (m, r)
    return (None, s)
  return NewParser

# e_parsers are a list of (parser, error messages)
def Sequence(*e_parsers):
  def NewParser(s):
    results = []
    original_string = s
    for (p, e) in e_parsers:
      (m, s) = p(s)
      results.append(m)
      if m is None:
        if e: raise SyntaxError("%s: %s"%(e, s))
        return (None, original_string)
    return (results, s)
  return NewParser


# Clean the result of the parser p, by applying the function f
def Clean(p, f):
  def NewParser(s):
    (m, r) = p(s)
    if m: return (f(m), r)
    return (None, s)
  return NewParser

