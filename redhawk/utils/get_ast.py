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

NOTE: The Close method must be called MANUALLY when using the
ASTFetcher class to update the database file.

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
import key_value_store as KVStore

import logging
import os
import shelve


def GetLAST(filename, database, key=None, language=None, store_new = True):
  """ Get a Single LAST. Similar to creating a LAST fetcher instance using
  CreateLASTFetcher, and then using GetAST."""
  last_parser = lambda filename: parse_ast.GetLAST(filename, language)
  if database == None:
    return last_parser(filename)

  ast_fetcher = CreateLASTFetcher(database, language, store_new = store_new)
  ast = ast_fetcher.GetAST(filename, key)
  ast_fetcher.Close()
  return ast



def GetLanguageSpecificTree(filename, database, key=None, language=None,
    store_new = True):
  """ Get a Single Language Specific Tree. Similar to creating a Language
  Specific Tree fetcher instance using CreateLanguageSpecificFetcher, and then
  using GetAST."""
  specific_parser = lambda filename: parse_ast.ParseFile(filename, language)
  if database is None:
    return specific_parser(filename)
  ast_fetcher = CreateLanguageSpecificFetcher(database, language, store_new = store_new)
  ast = ast_fetcher.GetAST(filename, key)
  ast_fetcher.Close()
  return ast

def CreateLASTFetcher(database, language = None, store_new = True):
  """ A factory method for creating a LAST fetcher (It handles the parser
  argument).

  The `database_file` argument is a path to the database file.  If None is passed as the
  `database_file` argument, the trees are ALWAYS reparsed.

  The `language` argument can be set to 'c' or 'python' if the `database_file` will
  contain only c files or python files respectively. If a mixture is to be
  stored, this is set to None. (The `language` argument exists only for
  performance reasons -- it avoids language detection.)
  
  If `store_new` is set, then the AST fetcher returned stores new trees it
  comes across."""
  
  return ASTFetcher(
      database_file = database, 
      parser = lambda filename: parse_ast.GetLAST(filename, language),
      store_new = store_new)


def CreateLanguageSpecificFetcher(database, language=None, store_new =
    True):
  """ A factory method for creating a language specific tree Fetcher.

  The `database_file` argument is a path to the database file. If None is
  passed, the trees are ALWAYS reparsed.

  The `language` argument can be set to 'c' or 'python' if the database_file
  will contain only c files or python files respectively. If a mixture is to
  be stored, this is set to None. (The `language` argument exists only for
  performance reasons -- it avoids language detection.)
  
  If `store_new` is set, then the AST fetcher returned stores new trees it
  comes across."""
  return ASTFetcher(
      database_file = database,
      parser = lambda filename: parse_ast.ParseFile(filename, language),
      store_new = store_new)


class ASTFetcher:
  """ Fetches AST trees from a database.

  Normally, you would want to use either of the factory functions:
    * CreateLASTFetcher - Get an instance of the AST class, that fetches
      Language agnostic parse trees.

    * CreateLanguageSpecificFetcher - Get an instance of the AST class that
      fetches language specific parse trees.

  NOTE: The Close method must be called MANUALLY. This is so for performance
  reasons. If this is cumbersome, because you are fetching only one LAST or
  one Language Specific Tree, use the helper functions, `GetLAST` and
  `GetLanguageSpecificTree` respecitively."""

  def __init__(self, database_file, parser, store_new = True):
    self.database_file = database_file
    self.parser = parser
    self.store_new = store_new
    # logging.info("Reading..\n")
    if self.database_file is None:
      self.database = None
      return

    if not os.path.exists(database_file):
      logging.warning("Database %s does not exist."%(self.database_file))
      self.database = None
      return

    if not KVStore.IsValidStore(database_file):
      print database_file
      logging.error("Not a valid store. Recreating..\n")
      KVStore.RemoveExistingStore(database_file)
      KVStore.CreateNewStore(database_file, redhawk.GetVersion())

    self.database = KVStore.KeyValueStore(database_file, redhawk.GetVersion())
    # logging.info("Done.")
    return


  def WriteDatabase(self):
    """ Update the database file."""
    if self.database:
      self.database.Write()

  def Close(self):
    if self.database:
      self.database.Close()

  def GetAST(self, filename, key=None):
    """ Extract a tree from the database. If `key` is None, the basename of
    the file is used. If the tree cannot be found, it is parsed, and stored in
    the database (in Memory).

    Note that to UPDATE the Database FILE, WriteDatabase() or Close() must be called.
    """
    if not self.database:
      return self.parser(filename)

    digest = util.GetHashDigest(filename)
    key = key or os.path.basename(filename)
  
    if self.database.HasKey(key):
      (pickled_digest, pickled_ast) = self.database.Get(key)
      if pickled_digest == digest:
        return pickled_ast
  
    if self.parser is None:
      return None
  
    ast = self.parser(filename)
    if self.store_new:
      self.database.Set(key, (digest, ast))
    return ast
