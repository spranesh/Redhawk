#!/usr/bin/env python

""" This module contains a redhawk commands that need to support
parallelisation. We call these tasks.

Currently, there are three tasks:


  * add
  * query
  * remove

due to large number of files they involve.

In order to use parallel python to parallelise them easily, we need to satisfy
the following constraints:

  * This module should have no 'as' or 'from' imports. All imports must be an
    absolute simple import statement.
 
  * All the imports in this module must be listed as strings in the IMPORTS
    list.

  * Each of the functions can take any number of arguments, but only the first
    will be `mapped` over. In other words, if f is a function that works on a
    list of files (say adds it to the database), and needs additional
    information like the database file, etc.., then:

      + f's first argument must be the list of files.
      + Instead of f(files, a, b, c...) being called,
        f(files_part1, a, b, c),
        f(files_part2, a, b, c),
        f(files_part3, a, b, c),
        etc.. will be called parallely.

  * No function within this module can be called by any of the Tasks. They may
    only refer to the imported modules.

The tasks in this module are to be executed through the TaskRunner class in
redhawk.utils.task_runner
"""

from __future__ import absolute_import
import redhawk.common.format_position
import redhawk.common.xpath
import redhawk.scripts.script_util
import redhawk.common.get_ast

IMPORTS = [
'redhawk.common.format_position',
'redhawk.common.xpath',
'redhawk.scripts.script_util',
'redhawk.common.get_ast']


def Query(files, database_file, parsed_query, store_new, context):
  """ Query all files in the iterator `files`, with the parsed_query.

  Use the `database_file` as the database. If store_new is set to True, store
  new files in the database.

  Print `context` number of lines on either of side of matching results.
  """
  ast_fetcher = redhawk.common.get_ast.CreateLASTFetcher(database_file, store_new = store_new)
  for f in files:
    key = redhawk.scripts.script_util.GetKey(f, database_file)
    ast = ast_fetcher.GetAST(f, key)
    results = set(redhawk.common.xpath.ApplyParsedXPathQuery([ast], parsed_query))

    if results:
      fp = open(f)
      lines = fp.readlines()
      fp.close()
      
      for r in results:
        redhawk.common.format_position.PrintContextInFile(r, context = context)

  ast_fetcher.Close()
  return
