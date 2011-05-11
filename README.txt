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

    $ redhawk '*/DefineFunction' file1.py file2.c

Redhawk is currently under heavy development. The code can be found on
`github`_. 

Redhawk currently requires python 2.6 or 2.7.

Project Objectives
------------------

(or what's coming up)

1. Allow users to effectively find and thereby navigate code in an
editor-independent manner.

2. Become fast enough to work on large code bases. Note that Redhawk already
works on Django, i.e., can be used to query code in Django. Using Redhawk
without a database, gives us a stream of steady but slow results. On the
other hand, if Redhawk is used with its custom pickle-database, it takes a
very long time to start, but throws up results very quickly. (The database
file is ~62MB in size). Techniques like splitting up the database into smaller
ones, are being looked at.

3. Sparkling documentation for API usage, and a long list of examples, with
examples scripts using the Selector API.

4. Allow cross-language analysis in the future, thereby benefitting projects
in multiple languages.

5. Expose the LAST in a simple manner via the Redhawk API for other tools.
These tools could involve indenting code, suggesting completions, or static
analysis.

6. Eventually allow editing of the LAST, and thereby powerful 
refactoring.


Dependencies
------------

*Runtime Dependencies*:

* `pycparser`_ is required to parse C code into ASTs. This
  in-turn depends on Python-PLY (`python-ply` on debian-ubuntu).

*Optional but highly recommended Dependencies*:

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

The `redhawk` program supports four commands:

=========   =======================================================
 Command      Purpose
=========   =======================================================
init        Create an EMPTY AST index.
add         Add files to an AST index.
query       Query for a pattern in a list of files, or in the index.
show        Show (visualize) a file either as text, or as an image.
prompt      Drop into a python prompt with helpful functions for 
            exploring the parse tree.
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
github.)[1]_ 

For the examples below, we shall use the `counter.py`_ file::

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

    counter.py:1:def CounterClosure(init=0):
    counter.py:16:def CounterIter(init = 0):

*Example 2*:
Let us find all functions one level below the module level in `counter.py`::

    $ redhawk query '*/DefineFunction' counter.py

This gives us::

    counter.py:9:def __init__(self, init=0):
    counter.py:12:def Bump(self):


*Example 3*:
Let us find all functions *anywhere* in the program.::

    $ redhawk query '**/DefineFunction' counter.py

This gives us::

    counter.py:3:def Inc():
    counter.py:9:def __init__(self, init=0):
    counter.py:12:def Bump(self):
    counter.py:1:def CounterClosure(init=0):
    counter.py:16:def CounterIter(init = 0):

(Note that this is not necessarily in a sorted order. This can be fixed by
passing the result through an invocation of sort.)

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

    counter.py:1:def CounterClosure(init=0):
    counter.py:16:def CounterIter(init = 0):


The `@{..}` represents a python lambda function, with the default variable n.
Thus, it is another way of providing arbitrary functions to match with. [2]_

*Example 7*:
Find all assignments where init is involved. Looking again at the `node`
configuration file, we realise that we are looking for `Assignment` Nodes, which
have a `ReferVariable` descendent, whose name is 'init'::

    $ redhawk query '**/Assignment/**/ReferVariable@[name="init"]' counter.py

This gives us::

    counter.py:2:value = [init]
    counter.py:10:self.value = init
    counter.py:18:init += 1

Note the `@[..]` syntax similar to XPATH, for referring to an attribute.

*Example 8*:
What if we wanted assignments were init was being set, and not referred to?

An abstract grammar of the query language can be found via::

    $ pydoc redhawk.common.xpath


Using the API
-------------

The `redhawk` package can also be used as an API by importing
`redhawk.common.selector` and related packages. Some of the useful packages
are already imported for the user in `redhawk_prompt` and are a good place to
start things at.


License
-------
Redhawk is distributed under the terms of the 2-clause BSD license. You are
free to use it for commercial or non-commercial projects with little or no
restriction. For a complete text of the license see the LICENSE.txt file in
the source distribution.


.. [1] `ast_gen.py`_ generates `node.py`_ and `types.py`_ using these YAML configuration files.
.. [2] In fact the portion inside the `@{..}` is just appended to a 'lambda n:' and `eval`-ed to get a function.

.. _imgur: http://imgur.com/CBHCX
.. _counter.py: https://github.com/spranesh/Redhawk/tree/master/redhawk/test/files/python/counter.py
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
.. _Python YAML: http://www.pyyaml.org
.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/1.0.0/

