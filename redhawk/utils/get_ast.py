#!/usr/bin/env python
""" This module contains procedures that are used to fetch Abstract Syntax
Trees, optionally using a database. The database is internally stored using
python pickle files.

There are two types of trees that are required.

1. The Language Agnostic Syntax Tree (LAST). This is the tree that redhawk
performs its operations on. This is what is required almost all of the time -
for querying, searching, editing (in upcoming versions), etc..

2. The various Language SPECIFIC trees. These are the trees emitted by the
parsers of the various languages - `pycparser`, the `ast` module in python,
etc.. These are used by Redhawk internally to CONSTRUCT the LAST. This is
almost never need by the API user. It is provided here since much of redhawk
internally requires it.

The ASTFetcher class is never instantiated directly. Instances of the
ASTFetcher class are created by calling either CreateLASTFetcher, or
CreateLanguageSpecificFetcher.

NOTE: The WriteDatabase method must be called MANUALLY when using the
ASTFetcher class to update the database file. This is so, for performance
reasons.


If a single tree is to be obtained, it is easier to call GetLAST, or
GetLanguageSpecificTree.

In short, only the GetLAST, and the CreateLASTFetcher functions are required
by most API users.

NOTE: None can be passed as the argument to the database argument, for any of
these functions. In such a case, it will simply fetch the required tree, by
parsing (and converting) it.
"""

import parse_ast
import redhawk
import util

import cPickle as P
import os
import sys

VERSION_KEY = '__redhawk__version__'


def GetLAST(filename, database, key=None, language=None):
  """ Get a Single LAST. Similar to creating a LAST fetcher instance using
  CreateLASTFetcher, and then using GetAST."""
  last_parser = lambda filename: parse_ast.GetLAST(filename, language)
  if database == None:
    return last_parser(filename)

  ast_fetcher = CreateLASTFetcher(database, language)
  ast = ast_fetcher.GetAST(filename, key)
  ast_fetcher.WriteDatabase()
  return ast



def GetLanguageSpecificTree(filename, database, key=None, language=None):
  """ Get a Single Language Specific Tree. Similar to creating a Language
  Specific Tree fetcher instance using CreateLanguageSpecificFetcher, and then
  using GetAST."""
  specific_parser = lambda filename: parse_ast.ParseFile(filename, language)
  if database is None:
    return specific_parser(filename)
  ast_fetcher = CreateLanguageSpecificFetcher(database, language)
  ast = ast_fetcher.GetAST(filename, key)
  ast_fetcher.WriteDatabase()
  return ast

def CreateLASTFetcher(database, language = None):
  """ A factory method for creating a LAST fetcher (It handles the parser
  argument).

  The `database_file` argument is a path to the database file.  If None is passed as the
  `database_file` argument, the trees are ALWAYS reparsed.

  The `language` argument can be set to 'c' or 'python' if the `database_file` will
  contain only c files or python files respectively. If a mixture is to be
  stored, this is set to None. (The `language` argument exists only for
  performance reasons -- it avoids language detection.)"""
  
  return ASTFetcher(
      database_file = database, 
      parser = lambda filename: parse_ast.GetLAST(filename, language))


def CreateLanguageSpecificFetcher(database, language=None):
  """ A factory method for creating a language specific tree Fetcher.

  The `database_file` argument is a path to the database file. If None is
  passed, the trees are ALWAYS reparsed.

  The `language` argument can be set to 'c' or 'python' if the database_file
  will contain only c files or python files respectively. If a mixture is to
  be stored, this is set to None. (The `language` argument exists only for
  performance reasons -- it avoids language detection.)"""
  return ASTFetcher(
      database_file = database,
      parser = lambda filename: parse_ast.ParseFile(filename, language))


class ASTFetcher:
  """ Fetches AST trees from a pickle file. 

  Normally, you would want to use either of the factory functions:
    * CreateLASTFetcher - Get an instance of the AST class, that fetches
      Language agnostic parse trees.

    * CreateLanguageSpecificFetcher - Get an instance of the AST class that
      fetches language specific parse trees.

  NOTE: The WriteDatabase must be called MANUALLY. This is so for performance
  reasons. If this is cumbersome, because you are fetching only one LAST or
  one Language Specific Tree, use the helper functions, `GetLAST` and
  `GetLanguageSpecificTree` respecitively."""

  def __init__(self, database_file, parser):
    self.database = database_file
    self.parser = parser
    self.changed = False
    self.parsed_data = self.__ReadFromDatabase()
    return

  def __ReadFromDatabase(self):
    try:
      fp = open(self.database)
      parsed_data = P.load(fp)
      fp.close()
    except (IOError, EOFError):
      sys.stderr.write("Could not read from database.\n")
      parsed_data = {}
      self.changed = True
    except TypeError:
      parsed_data = {}
      self.changed = True

    # If version numbers don't match, don't read the data.
    if (not parsed_data.has_key(VERSION_KEY) or
        parsed_data[VERSION_KEY] != redhawk.__version__):
      parsed_data = {}
      parsed_data[VERSION_KEY] = redhawk.__version__
      self.changed = True
    return parsed_data


  def __WriteToDatabase(self):
    # sys.stderr.write("Changed?%s\n"%(self.changed))
    if self.database is None:
      return
    if self.changed == False:
      return

    try:
      fp = open(self.database, "w")
      P.dump(self.parsed_data, fp)
      fp.close()
    except IOError, e:
      sys.stderr.write("Could not write to Database: No Write permissions?\n")
    self.changed = False
    return

  def WriteDatabase(self):
    """ Update the databse file."""
    return self.__WriteToDatabase()


  def GetAST(self, filename, key=None):
    """ Extract a tree from the database. If `key` is None, the basename of
    the file is used. If the tree cannot be found, it is parsed, and stored in
    the database (in Memory).

    Note that to UPDATE the Database FILE, WriteDatabase() must be called.
    """
    digest = util.GetHashDigest(filename)
    key = key or os.path.basename(filename)
  
    if self.parsed_data.has_key(key):
      (pickled_digest, pickled_ast) = self.parsed_data[key]
      if pickled_digest == digest:
        return pickled_ast
  
    if self.parser is None:
      return None
  
    ast = self.parser(filename)
    self.parsed_data[key] = (digest, ast)
    self.changed = True
    return ast
