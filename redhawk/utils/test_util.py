import nose.tools
import util as U

def TestConcat():
  assert(U.Concat([[1], [2, 3], [4, 5]]) == [1, 2, 3, 4, 5])
  assert(U.Concat([[1], [2, 3], [4, 5]]) == [1, 2, 3, 4, 5])
  assert(U.Concat([[]]) == [])
  return


def TestFlatten():
  assert(U.Flatten([1, 2, 3, 4]) == [1, 2, 3, 4])
  assert(U.Flatten([[1], [2, 3], 4]) == [1, 2, 3, 4])
  assert(U.Flatten([[1], [[2, 3]], 4]) == [1, 2, 3, 4])

  assert(U.Flatten([[1], [[[2]]], 3]) == [1, 2, 3])


def TestGuessLanguageSuccess():
  assert(U.GuessLanguage('foo.py') == 'python')
  assert(U.GuessLanguage('foo.c') == 'c')

  assert(U.GuessLanguage('foo.blah.py') == 'python')
  assert(U.GuessLanguage('foo.blah.c') == 'c')


def TestIfElse():
  # Test basic behaviour
  assert(U.IfElse(True, 2, 3) == 2)
  assert(U.IfElse(False, 2, 3) == 3)

  # Test lazy behaviour of condition
  assert(U.IfElse(lambda: True, 2, 3) == 2)
  assert(U.IfElse(lambda: False, 2, 3) == 3)

  # Test lazy behaviour of return values
  assert(U.IfElse(True, lambda: 2, lambda: 3) == 2)
  assert(U.IfElse(False, lambda: 2, lambda: 3) == 3)

  # Test all lazy behaviour
  assert(U.IfElse(lambda: True,
                lambda: 2,
                lambda: 3) == 2)
