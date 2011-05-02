#!/usr/bin/env python
import redhawk.common.selector as S
import redhawk.common.position as P
import redhawk.common.writers.dot_writer as D
import redhawk.common.writers.xml_writer as X
import redhawk.utils.get_ast as G
import redhawk.utils.util as U

import optparse
import os
import sys
import tempfile
import webbrowser

def GetOptions():
  default_string = " [default: %default]"
  parser = optparse.OptionParser()
  parser.add_option('-p',
          action='store',
          dest='pickle_file',
          type='string',
          default='/tmp/redhawk.pickle',
          help = 'File to store and fetch Pickled asts from.' + default_string)

  options, args = parser.parse_args()
  return options, args

def ConvertFileToAst(f, pickle_file=None):
  """ Convert a file into an language agnostic AST."""
  return G.GetLAst(f, pickle_file)

def ConvertCodeToAst(s, language, pickle_file):
  """ Convert a code snippet into an language agnostic AST."""
  (fp, name) = tempfile.mkstemp(suffix='.' + language, text=True)
  fp.write(s)
  fp.close()
  return ConvertFileToAst(name, pickle_file)


def Main():
  options, args = GetOptions()
  if args is None:
    trees = []
  else:
    trees = [ConvertFileToAst(f, options.pickle_file) for f in args]
  return EnterShell(trees)


def ShowAST(ast, eog=False):
  """ Show the given ast as an image."""
  temp_name = tempfile.mktemp(suffix='.png')
  D.WriteToImage(ast, filename=temp_name)
  return ShowImage(temp_name, eog)


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


def Help(display=True):
  s = """

Built in Variables:
    trees - contains the parse trees of the files passed in the command line

Built in Functions:
    ConvertFileToAst - Converts a file into a language agnostic AST.
    ConvertCodeToAst - Converts a code snippet into a language agnostic AST.
    Help             - Displays this prompt.
    ShowAST          - Shows the AST as a graph using dot.

Built in Modules:
    S - redhawk.common.selector 
    P - redhawk.common.position 
    X - redhawk.common.writers.xml_writer

To view this again, use the Help function.  """

  if display:
    print s
  else:
    return s
  

def EnterShell(trees):
  local_vars = {
      'trees' : trees,
      'ConvertFileToAst': ConvertFileToAst,
      'ConvertCodeToAst': ConvertCodeToAst,
      'Help':Help,
      'ShowAST':ShowAST,
      'S':S,
      'P':P,
      't': trees[0],
      'X': X}
  U.StartShell(local_vars, banner=Help(display=False))


if __name__ == '__main__':
  Main()
