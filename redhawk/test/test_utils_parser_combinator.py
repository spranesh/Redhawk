""" Test the parser_combinator.py in redhawk/utils."""

import nose.tools
import redhawk.utils.parser_combinator as P
import re

digits = re.compile("[0-9]+")
bracketed = re.compile("{[^}]*}")


def TestLiteral():
  assert(P.Literal("a")("abcd") == ("a", "bcd"))
  assert(P.Literal("ab")("abcd") == ("ab", "cd"))
  assert(P.Literal("a")("bcd")  == (None, "bcd"))
  assert(P.Literal("abcd")("abcd")  == ("abcd", ""))

def TestRegex():
  assert(P.Regex(digits)("01231abcd") == ("01231", "abcd"))
  assert(P.Regex(digits)("abcd") == (None, "abcd"))

  assert(P.Regex(bracketed)("{asdfa}") == ("{asdfa}", ""))
  assert(P.Regex(bracketed)("{asdfa}gh") == ("{asdfa}", "gh"))
  assert(P.Regex(bracketed)("{}") == ("{}", ""))
  assert(P.Regex(bracketed)("a{}") == (None, "a{}"))

@nose.tools.raises(AssertionError)
def TestRegexWithNonRegexObject():
  P.Regex("foobar")

def TestFinished():
  assert(P.Finished()("") == ("", ""))
  assert(P.Finished()("foobar") == (None, "foobar"))

def TestMaybe():
  digits_parser = P.Maybe(P.Regex(digits))
  assert(digits_parser("asdf012") == ("", "asdf012"))

  digits_parser = P.Maybe(P.Regex(digits), lambda: list())
  assert(digits_parser("asdf012") == ([], "asdf012"))

def TestOnePlus():
  single_digit_parser = P.Regex(re.compile("[0-9]"))
  digits_parser = P.OnePlus(single_digit_parser)

  assert(digits_parser("01231") == (list("01231"), ""))
  assert(digits_parser("a01231") == (None, "a01231"))

def TestSequence():
  a, b, c = map(P.Literal, list("abc"))
  abc_parser = P.Sequence(
      (a, None),
      (b, None),
      (c, None))
  assert(abc_parser("abc") == (list("abc"), ""))
  assert(abc_parser("abcdef") == (list("abc"), "def"))
  assert(abc_parser("abdef") == (None, "abdef"))
  assert(abc_parser("foobar") == (None, "foobar"))

@nose.tools.raises(SyntaxError)
def TestSequenceFailure():
  a, b, c = map(P.Literal, list("abc"))
  abc_parser = P.Sequence(
      (a, None),
      (b, "b was expected to be found"),
      (c, None))
  abc_parser("acc")

def TestClean():
  int_parser = P.Clean(P.Regex(digits), lambda x: int(x))
  assert(int_parser("01213") == (1213, ""))
  assert(int_parser("5f") == (5, "f"))
  assert(int_parser("f5") == (None, "f5"))
