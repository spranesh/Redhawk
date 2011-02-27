import pycparser
import sys

def ShowObject(a):
  for name in dir(a):
    if name[:2] != "__":
      print ("%10s : %s"%(name, str(getattr(a, name))))
  return

def StartShell():
  try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell(local_ns=locals())
  except ImportError:
    code.interact(local=locals())

try:
  filename = sys.argv[1]
except IndexError, e:
  sys.stderr.write("No C file specified to parse.\n")
  sys.exit(1)

tree = pycparser.parse_file(filename, use_cpp = True, cpp_path='cpp', cpp_args='-Ifake_libc_include')
body = tree.children()
program = open(filename).read()
if "show" in sys.argv:
  tree.show()
else:
  StartShell()
