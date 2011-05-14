=======
Redhawk
=======

Redhawk is a code navigation system built on the idea of a language agnostic
parse tree. It currently supports C & Python.

Code navigation systems are few and far. They are either too tied to a
language, or are very heuristic in nature --- using regex based parsers.
Redhawk attempts to acheive the best of both worlds. It uses standard, robust,
parsers each of the languages, and converts the resulting AST to a language
agnostic AST, or LAST.

The resulting LAST can be queried by using either Selectors (similar to
JQuery), or an xpath like syntax. A Typical use of Redhawk is as shown below::

    $ redhawk query '*/DefineFunction' file1.py file2.c

Redhawk is currently under heavy development. The code can be found on
`github`_. 

Redhawk currently requires python 2.6 or 2.7.

NOTE: From Version 1.1.2 onwards, Redhawk supports parallel querying using the
parallel-python (pp) module. This speeds up Redhawk's querying on large
codebases. Querying for closures anywhere in Django (~2200 files) can now be
done in ~20 seconds on a celeron netbook.

Project Objectives
------------------

(or what's coming up)

1. Allow users to effectively find and thereby navigate code in an
editor-independent manner.

2. Better documentation for API usage, and a long list of examples, with
examples scripts using the Selector API.

3. Allow cross-language analysis in the future, thereby benefitting projects
in multiple languages.

4. Expose the LAST in a simple manner via the Redhawk API for other tools.
These tools could involve indenting code, suggesting completions, or static
analysis.

5. Eventually allow editing of the LAST, and thereby powerful 
refactoring.


Dependencies
------------

*Runtime Dependencies*:

* `pycparser`_ is required to parse C code into ASTs. This
  in-turn depends on Python-PLY (`python-ply` on debian-ubuntu).

*Optional but highly recommended Dependencies*:

* `pp`_ - Parallel Python is required for running queries in parallel. This
  speeds up queries by more than 2x. This is highly recommended if you are
  going to query large projects. The whole of Django can be queried in less
  than 20 seconds, by using parallel python (passing `-p` to the `query`
  command).

* `Python Graphviz`_ is required for generating pretty AST graphs.  This
  package is an *optional* dependency, but highly recommended. This package goes by the name
  `python-pygraphviz` on Ubuntu, and depends on `graphviz`, and `dot`. (`Pip`
  seems to have a hard time install pygraphviz. Either `easy_install` or
  installing from your distribution's package manager should work).

*Development (Compile-time) Dependencies*:

* `Python YAML`_ is required for generating the AST classes in node.py
  form a simple configuration file. This goes by the name python-yaml on
  debian/ubuntu.

* `nosetests`_ is required for running the test suite.


Installing
----------

`pip` is the recommended tool to install Redhawk. It goes by `python-pip` on
debian/ubuntu and `pip`_ on the Python Package Index. The command::

    $ sudo pip install redhawk

should install redhawk, along with its dependency - pycparser. 

It is however recommended that you install the other packages also::

    $ sudo easy_install pygraphviz
    $ sudo pip install nose 'PyYAML>=3.09' 'nose>=0.11'

or by using your distribution's package manager. On Ubuntu/Debian (Ubuntu
Lucid seems to have new enough packages)::

    $ sudo aptitude install python-pygraphviz python-yaml python-nose
  

Notes
-----

1. Run `_build_tables.py` in the pycparser directory, to pre-generate the lex
and yacc tables. This will enable quicker parsing of C files. If pycparser was installed for all users, then 
 
  * Root priviliges may be required to run _build_tables.py 
  * Permissions for the resulting `lextab.py` and `yacctab.py` must be changed
    to allow all users to read (755).

You can find more about this `here`_.


Using Redhawk
-------------

Redhawk can be used from either the `redhawk` executable, or via the redhawk
API.

1. Using the `redhawk` program.
2. Using the Redhawk API via `import redhawk`


Using the `redhawk` executable
------------------------------

The `redhawk` program supports eight commands:

=========   =======================================================
 Command      Purpose
=========   =======================================================
add         Add files to an AST index.
init        Create an EMPTY AST index.
listfiles   List all the files in the AST index.
prompt      Drop into a python prompt with helpful functions for 
            exploring the parse tree.
query       Query for a pattern in a list of files, or in the index.
remove      Remove files from the AST index.
show        Show (visualize) a file either as text, or as an image.
where       Print the location of the current redhawk index (if there is one).
=========   =======================================================

The simplest way to run `redhawk` is to simply use a `query` command on a file
(or directory). The `query` command as described above takes an xpath-like
query, and a list of files (or directories), and searches for matches.

In the case that the set of files is large and is to be repeatedly queried, a
`redhawk` Language Agnostic Tree (LAST) database can be created using the
`redhawk init` command. Files in the project can be added to the database
using the `redhawk add` command.

The `show` command helps visualise the internal LAST structure used. The
command::

    $ redhawk show file.c

will show the LAST of `file.c` in a lisp/scheme like (sexp) syntax. A more
descriptive helpful visualisation can be obtained using the `-i` (or `-e`)
flags, which show graphs (generated using `graphviz` using the
`python-graphviz` module). This *requires* the pygraphviz module, an optional
though recommended, dependency. The command::

    $ redhawk show file.c -i

shows a graph using the default image python libraries.

The `prompt` command drops you into a prompt for exploring and querying the
LAST. This enables the use of selectors, a very powerful method for finding
what you want. For more information on selectors, see::

    $ pydoc redhawk.common.selector

for detailed documentation.

Introduction to the Query Language
----------------------------------

The `query` command supports an XPATH-like language for querying. We describe
examples below. In querying for a particular construct, the name of that Node
in the LAST has to be known. (Thorough documentation about this is coming up.
For now, one can refer to the `node`_ and `types`_ yaml configuration files on
github.) [1]_ 

For the examples below, we shall use the `counter.py`_ file. It is to be noted
that the same queries will work with other languages also (only C is supported
for now).::

     1	def CounterClosure(init=0):
     2	  value = [init]
     3	  def Inc():
     4	    value[0] += 1
     5	    return value[0]
     6	  return Inc
     7	
     8	class CounterClass:
     9	  def __init__(self, init=0):
    10	    self.value = init
    11	
    12	  def Bump(self):
    13	    self.value += 1
    14	    return self.value
    15	
    16	def CounterIter(init = 0):
    17	  while True:
    18	    init += 1
    19	    yield init
    20	
    21	if __name__ == '__main__':
    22	  c1 = CounterClosure()
    23	  c2 = CounterClass()
    24	  c3 = CounterIter()
    25	  assert(c1() == c2.Bump() == c3.next())
    26	  assert(c1() == c2.Bump() == c3.next())
    27	  assert(c1() == c2.Bump() == c3.next())
    28	  


Try `redhawk show` on the above file, to get a feel of its structure. You can
view the graphviz generated graph at `imgur`_.

*Example 1*:
Let us find all functions at the module level in `counter.py`::

    $ redhawk query 'DefineFunction' counter.py

This gives us::

    counter.py:16:def CounterIter(init = 0):
    counter.py:1:def CounterClosure(init=0):


Note:

1. The results are not necessarily in a sorted order, with respect to
   line number. This does not hamper the use of Redhawk for searching and
   navigation. (The results will always be guaranteed to be sorted with respect to the
   files). On the plus side, this makes Redhawk a little bit faster. If order is
   required, a simple invocation of the unix `sort` program should fix this.

2. The above query would work on a C program as well. Running the same query
   on `stats.c`_ gives us::

    stats.c:17:float Variance(float *p, int len)
    stats.c:5:float Mean(float *p, int len)
    stats.c:34:int main()

*Example 2*:
Let us find all functions one level below the module level in `counter.py`::

    $ redhawk query '*/DefineFunction' counter.py

This gives us::

    counter.py:9:def __init__(self, init=0):
    counter.py:3:def Inc():
    counter.py:12:def Bump(self):


*Example 3*:
Let us find all functions *anywhere* in the program.::

    $ redhawk query '**/DefineFunction' counter.py

This gives us::

    counter.py:9:def __init__(self, init=0):
    counter.py:16:def CounterIter(init = 0):
    counter.py:3:def Inc():
    counter.py:1:def CounterClosure(init=0):
    counter.py:12:def Bump(self):

*Example 4*:
Suppose we wanted to find all closures in the file. We could do this via::

    $ redhawk query '**/DefineFunction/**/DefineFunction' counter.py

This gives us::

    counter.py:3:def Inc():

*Example 5*:
Let us find all functions whose name starts with 'Counter'. Looking at the
`node` yaml configuration tells us that `DefineFunction` has an argument called
name. Now we simply need to test whether the first 7 letters of the name are
"Counter"::

    $ redhawk query '**/DefineFunction@{n.name[:7] == "Counter"}' counter.py

This gives us:

    counter.py:16:def CounterIter(init = 0):
    counter.py:1:def CounterClosure(init=0):


The `@{..}` represents a python lambda function, with the default variable n.
Thus, it is another way of providing arbitrary functions to match with. [2]_

To remind the reader that all these queries are langauge agnostic, running the
above command, but instead search for all functions that have the letter `e` in
the them, in the `stats.c`_ file.::

    $ redhawk query '**/DefineFunction@{n.name.find("e") != -1}' stats.c

gives us::

    stats.c:17:float Variance(float *p, int len)
    stats.c:5:float Mean(float *p, int len)

*Example 7*:
Find all assignments where init is involved. Looking again at the `node`
configuration file, we realise that we are looking for `Assignment` Nodes, which
have a `ReferVariable` descendent, whose name is 'init'::

    $ redhawk query '**/Assignment/**/ReferVariable@[name="init"]' counter.py

This gives us::

    counter.py:2:value = [init]
    counter.py:18:init += 1
    counter.py:10:self.value = init

Note the `@[..]` syntax similar to XPATH, for referring to an attribute.

*Example 8*:
What if we wanted assignments were init was being set, and not referred to? We
would use a code block to look at the `lvalue` of the `Assignment`.::

    $ redhawk query '**/Assignment@{n.lvalue.name == "init"}' counter.py

This gives us::

    counter.py:18:init += 1

*Example 9*:
Let us find all Function calls that start with 'Counter'. Looking again at the
`node`_ yaml configuration, we see that we want to find 'CallFunction's, where
the function object has a name starting with "Counter". [3]_ ::

    $ redhawk query '**/CallFunction@{n.function.name[:7] == "Counter"}' counter.py

This gives us::

    counter.py:24:c3 = CounterIter()
    counter.py:22:c1 = CounterClosure()
    counter.py:23:c2 = CounterClass()


An abstract grammar of the query language can be found via::

    $ pydoc redhawk.common.xpath

Much more is possible, using the Selector API.

Using the API
-------------

The `redhawk` package can also be used as an API by importing
`redhawk.common.selector` and related packages. Some of the useful packages
are already imported for the user in `redhawk prompt` and are a good place to
start things at.

*Example 1*:
Suppose in the above file we wanted to find all generators, i.e, function
definitions, which had a yield as a descendent. We shall see how easy, and
logical this query becomes using selectors.

We first go into a redhawk prompt::

    $ redhawk prompt counter.py                                                                [1]
    

We are greeted with a help banner::

    Built in Variables:
        trees - contains the parse trees of the files passed in the command line
    
    Built in Functions:
        ConvertFileToAst - Converts a file into a language agnostic AST.
        ConvertCodeToAst - Converts a code snippet into a language agnostic AST.
        Help             - Displays this prompt.
        ShowASTAsImage   - Shows the AST as a graph using dot.
    
    Built in Modules:
        S - redhawk.common.selector
        F - redhawk.common.format_position
    
    To view this again, use the Help function.
    

In the prompt, we define our selectors. (See `pydoc redhawk.common.selector`
for what selectors are, and how they can be composed)::

    In [1]: function_def = S.S(node_type='DefineFunction')
    In [2]: yield_stmt = S.S(node_type='Yield')
    In [3]: reqd_selector = function_def.HasDescendant(yield_stmt)


We then apply the selector on the file. The asts of the files passed are in
the `trees argument`. Since this file was the first, it is in `trees[0]`::

    In [4]: results = list(reqd_selector(trees[0]))
    In [5]: results[0]

gives us::

    Out[5]: DefineFunction


This is indeed the function we wanted. Just to be sure, we use the
`F.PrintContextInFile` function to print the context of the tree.::

    In [6]: F.PrintContextInFile(results[0], context=6)
    counter.py:10:       self.value = init
    counter.py:11:   
    counter.py:12:     def Bump(self):
    counter.py:13:       self.value += 1
    counter.py:14:       return self.value
    counter.py:15:   
    counter.py:16: > def CounterIter(init = 0):
    counter.py:17:     while True:
    counter.py:18:       init += 1
    counter.py:19:       yield init
    counter.py:20:   
    counter.py:21:   if __name__ == '__main__':
    counter.py:22:     c1 = CounterClosure()


It is easy to see from this example that selectors are highly composable, and
thus are very powerful. It is hoped that using selectors becomes a natural way
to write powerful custom scripts, for querying code.

License
-------
Redhawk is distributed under the terms of the 2-clause BSD license. You are
free to use it for commercial or non-commercial projects with little or no
restriction. For a complete text of the license see the LICENSE.txt file in
the source distribution.

Change List
------------

*v1.1.2*

* Redhawk can now use parallel python (on the same machine), to perform
  queries on codebases. This speeds up Redhawk (almost) proportionally to the
  number of cores you have on your computer. Redhawk can now query for
  closures in Django in just ~20 seconds.

* Friendlier usage strings and help messages.

*v1.1.1*

* Python2.7 compatibility: ast.parse (Thanks to Nafai77)

* Profiled, performance improvements by 15% by shifting to deque, and caching
  flattened children.

* Provided a bin/start_simple_bash_with_redhawk_in_pythonpath.sh to enter a
  temporary shell with redhawk in PYTHONPATH (for devs).

*v1.1.0*

* Fast enough to work on Django - Querying DefineClass anywhere in the
  codebase (~2300 python files), takes just 45 seconds on a celeron netbook.
  Thats 19ms per file!

* Uses the shelve module instead of the pickle module, to decrease read and
  write times for the redhawk database.

* Redhawk supports three new commands - `listfiles`, `remove`, `where`
 
* The `query`, and `show`, commands take an extra argument `-s`, to decide if
  new trees should be added to the database.

* Skip a file if there is a parser error.

.. [1] `ast_gen.py`_ generates `node.py`_ and `types.py`_ using these YAML configuration files.

.. [2] In fact the portion inside the `@{..}` is just appended to a 'lambda n:' and `eval`-ed to get a function.

.. [3] Note that 'CallFunction's do not directly have a name. This is because the function object, unlike that of a function definition, can be a value. It is possible to do (f.g[x])(y), and such.


.. _imgur: http://imgur.com/CBHCX
.. _counter.py: https://github.com/spranesh/Redhawk/tree/master/redhawk/test/files/examples/counter.py
.. _stats.c: https://github.com/spranesh/Redhawk/tree/master/redhawk/test/files/examples/stats.c
.. _ast_gen.py: https://github.com/spranesh/Redhawk/blob/master/redhawk/common/_ast_gen.py
.. _node.py: https://github.com/spranesh/Redhawk/blob/master/redhawk/common/node.py
.. _types.py: https://github.com/spranesh/Redhawk/blob/master/redhawk/common/types.py
.. _node: https://github.com/spranesh/Redhawk/blob/master/redhawk/common/_node_cfg.yaml
.. _types: https://github.com/spranesh/Redhawk/blob/master/redhawk/common/_types_cfg.yaml
.. _here: http://pycparser.googlecode.com/hg/README.html#installation-process
.. _pip: http://pypi.python.org/pypi/pip
.. _github: http://www.github.com/spranesh/Redhawk
.. _Python Graphviz: http://networkx.lanl.gov/pygraphviz/
.. _pycparser: http://code.google.com/p/pycparser/ 
.. _pycparser: http://pypi.python.org/pypi/pp
.. _Python YAML: http://www.pyyaml.org
.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/1.0.0/
