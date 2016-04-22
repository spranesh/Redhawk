#!/usr/bin/env python

""" This module implements a TaskRunner class, which can be used to run
tasks, such as those in redhawk.scripts.tasks.

This allows easy switching between running a task normally, and in parallel.

The first argument of a task is expected to be an iterable, which will be
chunked, before calling the workers in case of a parallel task run.
"""

from __future__ import absolute_import
import os
import sys

pp_not_found_error = """
The pp (parallel python) module was not found. If you have installed it,
please ensure that it is in python's path, by entering a python prompt, and
trying 'import pp'.

If you don't have it, you can get it from:

http://www.parallelpython.com/ or http://pypi.python.org/pypi/pp

You can also get it from pip:

  $ pip install pp

Please run redhawk without the parallel option in the meantime.
"""

class TaskRunner:
  def __init__(self,
      task,
      parallel=False,
      num_workers=0,
      chunk=80,
      servers = None,
      module_deps = None,
      function_deps = None,
      verbose = False):
    """ Create an instance of the Task Runner class.

    If parallel is False, the `task` is run on the args (see __call__).  Else,

    Else, `num_workers` are created, and the first element of args (which should
    be an iterable) is chunked into `chunk` sizes. If `num_workers` is 0, it
    is auto detected.

    `module_deps` are a tuple of modules that the task depends on.
    `function_deps` are a tuple of functions that the task depends on.
    """

    self.task = task
    self.parallel = parallel

    self.num_workers = num_workers or "autodetect"
    self.servers = servers or ()
    self.chunk = chunk

    if function_deps:
      self.function_deps = tuple(function_deps)
    else:
      self.function_deps = ()

    if module_deps:
      self.module_deps = tuple(module_deps)
    else:
      self.module_deps = ()

    self.verbose = verbose

    if parallel:
      try:
        import pp
      except ImportError as e:
        sys.stderr.write(pp_not_found_error)
        sys.exit(1)

      self.pp = pp
    return


  def __call__(self, *args):
    if self.parallel:
      args = list(args)
      if type(args[0]) is not list:
        args[0] = list(args[0])
      return self.RunParallel(args)
    else:
      return self.RunNormal(args)


  def RunNormal(self, args):
    """ Run the `task` normally."""
    return self.task(*args)


  def RunParallel(self, args):
    job_server = self.pp.Server(
        ncpus = self.num_workers,
        ppservers = self.servers,
        secret='redhawk-secret-key')

    if self.verbose:
      sys.stderr.write("Starting pp with %s workers\n"%(job_server.get_ncpus()))

    jobs = []

    load = args[0]
    dispatched = 0

    while dispatched < len(load):
      args[0] = load[dispatched : dispatched+self.chunk]
      dispatched += self.chunk

      jobs.append(job_server.submit(
        self.task,
        tuple(args),
        self.function_deps,
        self.module_deps,
      ))
    
    results = [job() for job in jobs]

    if self.verbose:
      fp = sys.stdout
      sys.stdout = sys.stderr
      job_server.print_stats()
      sys.stdout = fp

    job_server.destroy()
    return results
