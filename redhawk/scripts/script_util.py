#!/usr/bin/env python

""" Functions and Constants common to all the executables."""
import redhawk.utils.util as U

import string
import sys
import os
import tempfile

PYGRAPHVIZ_NOT_FOUND = """This feature requires the pygraphviz, which does not
seem to be installed.

It can be obtained using easy_install from http://pypi.python.org/pypi/pygraphviz
or from the distro's native package manager. pygraphviz goes by the name
python-pygraphviz on debian/ubuntu."""

# The standard Redhawk Database file.
DB_NAME = '.redhawk_db'

# The program name
PROGRAM_NAME = sys.argv[0]

# Default string passed at the end of help in optparse
OPTIONS_DEFAULT_STRING = "[default: %default]"

def ShowImage(filename, eog=False):
  if eog:
    os.system('eog %s'%(filename))
    return

  try:
    import Image
  except ImportError, e:
    print "Cannot find the Image module. Opening in your web-browser."
    webbrowser.open(filename)
    return
  
  im = Image.open(filename) 
  im.show()
  return

def ShowASTAsImage(ast, eog=False):
    try:
      import redhawk.common.writers.dot_writer as D
    except ImportError, e:
      ExitWithError(PYGRAPHVIZ_NOT_FOUND + "\n\nError: " + str(e))

    temp_name = tempfile.mktemp(suffix='.png')
    D.WriteToImage(ast, filename=temp_name)
    ShowImage(temp_name, eog)
    return


def MakeStringFromTemplate(template):
  """ Convert the template into a string, by substituting for $prog and
  $db."""
  return string.Template(template).safe_substitute(
      prog=PROGRAM_NAME,
      db=DB_NAME)

def ExitWithError(s, error_code = 1):
  """A quieter version of redhawk.utils.util's ExitWithError"""
  sys.stderr.write(s+"\n")
  sys.exit(error_code)

def IsFileSupported(filepath):
  """ Returns True if the file at `filepath` is supported by Redhawk. Else,
  returns False"""
  try:
    U.GuessLanguage(filepath)
  except KeyError, e:
    return False
  except ValueError, e:
    return False
  return True


def GetSupportedFiles(paths):
  """ Return a list of files, (after walking through directories), that are
  supported by redhawk."""
  for p in paths:
    if os.path.isdir(p):
      for root, dirs, files in os.walk(p):
        if '.git' in dirs: dirs.remove('.git')  # don't visit git directories
        for f in files:
          path = os.path.join(root, f)
          if IsFileSupported(path):
            yield path

    if os.path.isfile(p):
      if IsFileSupported(p):
        yield p



def GetDatabase():
  """ Return the location to the redhawk database if any."""
  try:
    return U.FindFileInDirectoryOrAncestors(DB_NAME, os.curdir)
  except IOError, e:
    sys.stderr.write("""The redhawk database exists, but does not have read & write
    permissions. Fix this to prevent re-parsing. Carrying on..""")
    return None


def GetKey(filepath, database):
  """ Return the key corresponding to the given filepath."""
  if not database: return None
  return U.AdjustFilePathToBaseDirectory(filepath, os.path.dirname(database))
