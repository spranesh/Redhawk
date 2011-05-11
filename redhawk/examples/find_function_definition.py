#!/usr/bin/env python
import redhawk.common.selector as S
import redhawk.utils.get_ast as G
import redhawk.utils.util as U

import sys

def Usage(n):
  sys.stdout.write("%s function-name [list-of-files]\n"%(sys.argv[0]))
  sys.exit(n)

def Main():
  if len(sys.argv) < 3:
    Usage(1)
  if "-h" in sys.argv:
    Usage(0)

  function_name = sys.argv[1]
  files = sys.argv[2:]

  asts = [G.GetLAST(x, database = None) for x in files]

  # Ugly way of writing the selector
  # selector = lambda x: x.GetName() == 'DefineFunction' and x.name == function_name

  # Neat way of writing the selector
  selector = S.Combine(
      S.NodeSelector('DefineFunction'),
      S.AttributeSelector(name = function_name))

  functions_wanted = U.Concat([list(S.Select(ast, selector)) for ast in asts])

  for f in functions_wanted:
    print f.position
  return


if __name__ == '__main__':
  Main()
