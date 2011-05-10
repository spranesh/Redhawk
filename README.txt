=======
RedHawk
=======

RedHawk is a code navigation system built on the idea of a language agnostic
parse tree. It currently supports C & Python. Code navigation systems are few
and far. They are either too tied to a language, or are very heuristic in
nature --- using regex based parsers. RedHawk attempts to acheive the best of
both worlds. It uses parses each of the languages, and converts the resulting
AST to a language agnostic AST, or L-AST.

The resulting L-AST can be queried by using either Selectors (similar to
JQuery), or an xpath like syntax. A Typical use of RedHawk is as shown below::

    $ redhawk '*/DefineFunction' file1.py file2.c

RedHawk is currently under heavy development. The code can be found on
`github`_. 

RedHawk currently requires python 2.6 or 2.7.

Project Objectives
------------------

1. Allow users to effectively find and thereby navigate code in an
editor-independent manner.

2. Enable users to write powerful queries to get to exactly where they want.

3. Allow cross-language analysis in the future, thereby benefitting projects
in multiple languages.

4. Expose the L-AST in a simple manner via the RedHawk API for other tools.
These tools could involve indenting code, suggesting completions, or static
analysis.

5. Eventually allow editing of the L-AST, and thereby powerful refactoring.


Dependencies
------------

*Runtime Dependencies*:

* `pycparser`_ - This is required to parse C code into ASTs. This
  in-turn depends on Python-PLY (`python-ply` on debian-ubuntu).

* `Python Graphviz`_ - For generating pretty AST graphs.  This package is an
  *optional* dependency. This package goes by the name `python-pygraphviz` on
  Ubuntu, and depends on `graphviz`, and `dot`.

*Development (Compile-time) Dependencies*:

* `Python YAML`_ - This is required for generating the AST classes in node.py
  form a simple configuration file. This goes by the name python-yaml on
  debian/ubuntu.


Installing
----------

`pip` is the recommended tool to install RedHawk. It goes by `python-pip` on
debian/ubuntu and `pip`_ on the Python Package Index. The command::

    $ sudo pip install redhawk

should install redhawk, along with its dependencies.


Using RedHawk
-------------

RedHawk can be used at least in three (increasingly powerful ways):

1. Using the `redhawk` program.
2. Using the `redhawk_prompt` program.
3. Using the RedHawk API via `import redhawk`


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

*Introduction to the Query Language*

The query langauge supported by redhawk is similar to XPATH.
-- MORE HERE --

Using the Redhawk Prompt
------------------------

The `redhawk_prompt` executable takes a file as an argument, and drops the
user into a python (or ipython) prompt with some ready imports, and a help
function. This is very useful for exploring the tree, and drafting some
complex queries using the selector API.

For more information on selectors, see::

    $ pydoc redhawk.common.selector

for detailed documentation.


Using the API
-------------

The `redhawk` package can also be used as an API by importing
`redhawk.common.selector` and related packages. Some of the useful packages
are already imported for the user in `redhawk_prompt` and are a good place to
start things at.


License
-------
RedHawk is distributed under the terms of the 2-clause BSD license. You are
free to use it for commercial or non-commercial projects with little or no
restriction. For a complete text of the license see the LICENSE.txt file in
the source distribution.

Notes
-----

1. Run `_build_tables.py` in the pycparser directory, to pre-generate the lex
and yacc tables. This will enable quicker parsing of C files. If pycparser was installed for all users, then 
 
  * Root priviliges may be required to run _build_tables.py 
  * Permissions for the resulting `lextab.py` and `yacctab.py` must be changed
    to allow all users to read (755).

2. `pip` seems to have problems installing `pygpraphviz` in a virtualenv. If
you don't know what a virtualenv is, you don't have to worry about this. This
is why `pygraphviz` is only an *OPTIONAL* dependency.

.. _pip: http://pypi.python.org/pypi/pip
.. _github: http://www.github.com/spranesh/Redhawk
.. _Python Graphviz: http://networkx.lanl.gov/pygraphviz/
.. _pycparser: http://code.google.com/p/pycparser/ 
.. _Python YAML: http://www.pyyaml.org
