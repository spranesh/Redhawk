#!/usr/bin/env python
import script_util as S

import redhawk.common.xpath as X
import redhawk.scripts.tasks as T
import redhawk.utils.task_runner as R

import optparse
import sys

usage = S.MakeStringFromTemplate("""$prog query [options] <query> file1 file2 ..

Use $prog query -h for help.

Brief description:
This command is used to query the ASTs.

For an introduction queries, see the redhawk homepage on PyPi -
http://pypi.python.org/pypi/redhawk

For a further discussion on queries, please read pydoc
redhawk.common.xpath (assuming redhawk is installed on your path).
""")

def QueryFilesJob(database_file, parsed_query, files, store_new, context):
  """ A wrapper around redhawk.scripts.query_core.QueryFiles.

  This wrapper serves as a job in parallel python."""
  return redhawk.scripts.query_core.QueryFiles(database_file,
      parsed_query, files, store_new, context)


def Main(args):
  parser = optparse.OptionParser(usage)

  parser.add_option(
      "-C",
      "--context",
      dest = "context",
      type = "int",
      default = 0,
      help = "Context to be shown." + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-n",
      "--no-database",
      action="store_false",
      dest="use_db",
      default=True,
      help = "Explicity tell redhawk to NOT use the database." 
      + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-s",
      "--store-new",
      action="store_true",
      dest="store_new",
      default=False,
      help = "Store new files that redhawk comes across in the database. "
      + "(implies no parallel)" 
      + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-p",
      "--parallel",
      action="store_true",
      dest="parallel",
      default=False,
      help = "Parallelise redhawk using the parallel python module (pp)."
      + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-w",
      "--workers",
      type = "int",
      dest = "workers",
      default = 0,
      help = "Number of workers to be used (applicable only if -p is used). "
      + "0 implies autodetect." 
      + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "--chunk",
      type = "int",
      dest = "chunk",
      default = 80,
      help = "Number of files passed in each chunk to a free worker (applicable only if -p is used)." 
      + S.OPTIONS_DEFAULT_STRING)

  options, args = parser.parse_args(args)
  if not len(args):
      parser.error("No query or files given.")

  if options.store_new:
    options.parallel = False

  parsed_query = X.ParseXPath(args[0])
  if len(args) == 1:
    sys.stderr.write("No files given\n\n")
    sys.stderr.write("Query was parsed as: %s\n"%(parsed_query))
    sys.exit(1)

  database_file = S.GetDatabase() if options.use_db else None
  files = args[1:]

  # def __init__(self,
  #     task,
  #     parallel=False,
  #     num_workers="autodetect",
  #     chunk=80,
  #     servers = None,
  #     module_deps = None,
  #     function_deps = None,
  #     verbose = False):

  runner = R.TaskRunner(T.Query,
      parallel=options.parallel,
      num_workers = options.workers,
      chunk = options.chunk,
      module_deps = T.IMPORTS)

  runner(S.GetSupportedFiles(files), database_file, parsed_query,
      options.store_new, options.context)
  return
