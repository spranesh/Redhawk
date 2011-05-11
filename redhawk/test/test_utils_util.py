""" Test the util.py in redhawk/utils."""

import redhawk.utils.util as U

import nose.tools
import tempfile
import os

def TestConcat():
  """ Test Concat."""
  assert(U.Concat([[1], [2, 3], [4, 5]]) == [1, 2, 3, 4, 5])
  assert(U.Concat([[1], [2, 3], [4, 5]]) == [1, 2, 3, 4, 5])
  assert(U.Concat([[]]) == [])
  return


def TestFlatten():
  """ Test Flatten."""
  assert(U.Flatten([1, 2, 3, 4]) == [1, 2, 3, 4])
  assert(U.Flatten([[1], [2, 3], 4]) == [1, 2, 3, 4])
  assert(U.Flatten([[1], [[2, 3]], 4]) == [1, 2, 3, 4])

  assert(U.Flatten([[1], [[[2]]], 3]) == [1, 2, 3])


def TestGuessLanguageSuccess():
  """ Test Guess Langague for Success."""
  assert(U.GuessLanguage('foo.py') == 'python')
  assert(U.GuessLanguage('foo.c') == 'c')

  assert(U.GuessLanguage('foo.blah.py') == 'python')
  assert(U.GuessLanguage('foo.blah.c') == 'c')


def TestIfElse():
  """ Test IfElse construct."""
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


def TestFindFileInDirectoryOrAncestors():
  """ Test FindFileInDirectoryOrAncestors"""
  # Create an empty temp directory
  root_dir = tempfile.mkdtemp()
  a_dir = os.path.join(root_dir, "a")
  b_dir = os.path.join(a_dir, "b")

  # Create subdirectories
  os.mkdir(a_dir)
  os.mkdir(b_dir)

  # Create temporary file
  filepath = os.path.join(root_dir, "test_file")
  fp = open(filepath, "w")
  fp.close()
  print root_dir, a_dir, b_dir, filepath

  # Check if test_file can be found
  assert(U.FindFileInDirectoryOrAncestors("test_file", b_dir) == 
      filepath)

  # Ensure that adding /. to the path does not 
  # change the result of the test
  c_dir = os.path.join(b_dir, os.path.curdir)
  assert(U.FindFileInDirectoryOrAncestors("test_file", c_dir) == 
      filepath)

  # Change Permissions to 000 and ensure that an
  # IOError is thrown
  os.chmod(filepath, 0)
  raised = False
  try:
    U.FindFileInDirectoryOrAncestors("test_file", c_dir)
  except IOError, e:
    raised = True
  assert(raised)

  # Remove the file and temporary directories
  os.remove(filepath)
  assert(U.FindFileInDirectoryOrAncestors("test_file", b_dir) == 
     None)
  os.removedirs(b_dir)
  return



