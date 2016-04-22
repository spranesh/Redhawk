#!/usr/bin/env python
""" 
Mapping of Various Parsers to languages.
"""

from __future__ import absolute_import
import redhawk.python.python_parser as python_parser
import redhawk.c.c_parser as c_parser
import redhawk.utils.util as U

language_parsers = {
 'c' : c_parser.CParser(),
 'python' : python_parser.PythonParser()
}

def GetParser(language = None, filename = None):
  """ Get the Parser for a particular language."""
  assert(language or filename)
  language = language or U.GuessLanguage(filename)
  return language_parsers[language]
