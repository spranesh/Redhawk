import redhawk.utils.util as U
import redhawk.utils.parse_asts as parse_asts

import sys

def ShowObject(a):
  for name in dir(a):
    if name[:2] != "__":
      print ("%10s : %s"%(name, str(getattr(a, name))))
  return

try:
  filename = sys.argv[1]
except IndexError, e:
  sys.stderr.write("No C file specified to parse.\n")
  sys.exit(1)

tree = parse_asts.ParseC(filename)
body = tree.children()
program = open(filename).read()
if "show" in sys.argv:
  tree.show(attrnames=True)
if "coord" in sys.argv:
  tree.show(showcoord=True)
else:
  U.StartShell(locals(), banner="Variables: tree, body, program, ShowObject")
