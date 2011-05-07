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

License
-------
RedHawk is distributed under the terms of the 2-clause BSD license. You are
free to use it for commercial or non-commercial projects with little or no
restriction. For a complete text of the license see the LICENSE.txt file in
the source distribution.

Notes
-----

1. Run `_build_tables.py` in the pycparser directory, to pre-generate the lex
and yacc tables, therey enabling quicker parsing of C files.

Dependencies
------------

*Runtime Dependencies*:

* `pycparser`_ - This is required to parse C code into ASTs. This
  in-turn depends on Python-PLY (`python-ply` on debian-ubuntu).

* `Python Graphviz`_ - For generating pretty AST graphs. This is an optional
  dependency. This package goes by the name `python-pygraphviz` on Ubuntu, and depends
  on `graphviz`, and `dot`.

*Development (Compile-time) Dependencies*:

* `Python YAML`_ - This is required for generating the AST classes in node.py
  form a simple configuration file. This goes by the name python-yaml on
  debian/ubuntu.


.. _github: http://www.github.com/spranesh/Redhawk
.. _Python Graphviz: http://networkx.lanl.gov/pygraphviz/
.. _Python C Parser: http://code.google.com/p/pycparser/ 
.. _Python YAML: http://www.pyyaml.org
