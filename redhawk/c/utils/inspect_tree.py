import redhawk.utils.util as U
import pycparser
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

tree = pycparser.parse_file(filename, use_cpp = True, cpp_path='cpp', cpp_args='-Ifake_libc_include')
body = tree.children()
program = open(filename).read()
if "show" in sys.argv:
  tree.show(attrnames=True)
if "coord" in sys.argv:
  tree.show(showcoord=True)
else:
  U.StartShell(locals(), banner="Variables: tree, body, program, ShowObject")
