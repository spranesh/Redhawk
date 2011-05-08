#!/usr/bin python
import optparse
import os
import string
import sys
import tempfile

try:
  import redhawk.utils.util as U
  import redhawk.utils.get_ast as G
except ImportError, e:
  print "Is redhawk installed on your python library path?\n\n?"
  print e
  sys.exit(1)


__DB_NAME__ = '.redhawk_db'
program_name = sys.argv[0]
options_default_string = "[default: %default]"

HELP = string.Template("""
Usage: $prog COMMAND [ARGS]

$prog - An AST based navigation system. 

The simplest use case is just:

  $ $prog query <query> files

Supported commands are:
  init        Create an EMPTY AST index.
  add         Add files to an AST index.
  query       Query for a pattern in a list of files, or in the index.
  show        Show (visualize) a file either as text, or as an image.

See $prog COMMAND --help for more detailed information about that command.

NOTE: The creation of an index for large projects is recommended. This can be
done with the init, and add commands.  Though recommended, an index is NOT
necessary.
""").safe_substitute(prog=program_name)



def ShowImage(filename, eog=False):
  if eog:
    os.system('eog %s'%(filename))
    return

  try:
    import Image
  except ImportError, e:
    print "Cannot find the Image module. Opening in your web-browser."
    webbrowser.open(filename)
    return
  
  im = Image.open(filename) 
  im.show()
  return


def GetDatabase():
  """ Return the location to the redhawk database if any."""
  try:
    return U.FindFileInDirectoryOrAncestors(__DB_NAME__, os.curdir)
  except IOError, e:
    sys.stderr.write("""The redhawk database exists, but does not have read & write
    permissions. Fix this to prevent re-parsing. Carrying on..""")
    return None


def GetKey(filepath):
  """ Return the key corresponding to the given filepath."""
  return U.AdjustFilePathToBaseDirectory(__DB_NAME__, os.curdir)


def IsFileSupported(filepath):
  try:
    U.GuessLanguage(filepath)
  except KeyError, e:
    return False
  except ValueError, e:
    return False
  return True


def GetSupportedFiles(paths):
  """ Return a list of files, (after walking through directories), that are
  supported by redhawk."""
  for p in paths:
    if os.path.isdir(p):
      for root, dirs, files in os.walk(p):
        if '.git' in dirs: dirs.remove('.git')  # don't visit git directories
        for f in files:
          path = os.path.join(root, f)
          if IsFileSupported(path):
            yield path

    if os.path.isfile(p):
      if IsFileSupported(p):
        yield p


def InitMain(args):
  usage = """%s init

  This command is used to create an empty index in the CURRENT directory.
  It takes no command line options. The AST index is stored in a file called
  %s.
  """%(program_name, __DB_NAME__)
  parser = optparse.OptionParser(usage)
  options, args = parser.parse_args(args)

  if len(args):
    parser.error("Extra options given. This command takes no options!")

  if os.path.exists(__DB_NAME__):
    U.ExitWithError("An AST index already exists.")

  try:
    fp = open(__DB_NAME__, "w")
    fp.write("")
    fp.close()
  except IOError, e:
    U.ExitWithError(e)
  return


def QueryMain(args):
  usage = """%s query [options] <query> file1 file2 ..

  This command is used to query the ASTs.


  <<< Insert Brief discussion on queries here

  For a further discussion on queries, please read pydoc
  redhawk.common.xpath (assuming redhawk is installed on your path).
  """
  try:
    import redhawk.common.xpath as X
    import redhawk.common.position as P
  except ImportError, e:
    ExitWithError(e)

  parser = optparse.OptionParser(usage)

  parser.add_option(
      "-C",
      "--context",
      dest = "context",
      type = "int",
      default = None,
      help = "Context to be shown." + options_default_string)

  parser.add_option(
      "-n",
      "--no-database",
      action="store_false",
      dest="use_db",
      default=True,
      help = "Explicity tell redhawk to NOT use the database." + options_default_string)

  options, args = parser.parse_args(args)
  if not len(args):
      parser.error("No query or files given.")

  parsed_query = X.ParseXPath(args[0])
  if len(args) == 1:
    sys.stderr.write("No files given\n\n")
    sys.stderr.write("Query was parsed as: %s\n"%(parsed_query))
    sys.exit(1)

  database = GetDatabase() if options.use_db else None

  files = args[1:]

  for f in GetSupportedFiles(files):
    ast = G.GetLAst(f, pickle_file = database, key=GetKey(f))
    results = list(X.ApplyParsedXPathQuery([ast], parsed_query))

    if options.context:
      # TODO(spranesh): Fix the context
      for r in results:
        p = P.GetPosition(r)
        print "+++%s:%d"%(f, p.line)
        print P.ShowPosition(p, context = options.context)

    else:
      fp = open(f)
      lines = fp.readlines()
      for r in results:
        p = P.GetPosition(r)
        print "%s:%d:%s"%(f, p.line, lines[p.line-1].strip())
      fp.close()
  return


def ShowMain(args):
  usage = """%s show [options] <query> <file>

  This command is used to show an AST. An AST can either be printed (default),
  or converted to an image (this requires python-graphviz).
  """

  parser = optparse.OptionParser(usage)

  parser.add_option(
      "-e",
      "--eog",
      action="store_true",
      dest="eog",
      default=False,
      help = "Show the AST as an image using Eye-of-gnome. (assumes -i)" + options_default_string)

  parser.add_option(
      "-i",
      "--image",
      action="store_true",
      dest="image",
      default=False,
      help = "Show the AST as an image." + options_default_string)

  parser.add_option(
      "-n",
      "--no-database",
      action="store_false",
      dest="use_db",
      default=True,
      help = "Explicity tell redhawk to NOT use the database." + options_default_string)

  options, args = parser.parse_args(args)
  if len(args) != 1:
      parser.error("Exactly one file should be given.")

  database = GetDatabase() if options.use_db else None


  ast = G.GetLAst(args[0], pickle_file = database, key=GetKey(args[0]))
  if options.eog:
    options.image = True

  if not options.image:
    print ast.ToStr()

  else:
    try:
      import redhawk.common.writers.dot_writer as D
    except ImportError, e:
      U.ExitWithError(e)

    temp_name = tempfile.mktemp(suffix='.png')
    D.WriteToImage(ast, filename=temp_name)
    ShowImage(temp_name, options.eog)
  return


def AddMain(args):
  usage = """%s add file1 file2 .. 

  Add ASTs to the database.
  """
  parser = optparse.OptionParser(usage)
  options, args = parser.parse_args(args)

  if not len(args):
      parser.error("No files given.")

  database = GetDatabase()

  if database is None:
    U.ExitWithError("No database found. Maybe %s init first?"%program_name)

  for f in GetSupportedFiles(args):
    ast = G.GetLAst(f, pickle_file = database, key=GetKey(f))
    print "%s: Added"%f
  return


def Main():
  if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print HELP
    sys.exit(0)

  dispatch = { 'init': InitMain,
               'query': QueryMain,
               'show': ShowMain,
               'add': AddMain}
  try:
    dispatch[sys.argv[1]](sys.argv[2:])
  except KeyError:
    print "Command %s not found."%sys.argv[1]
    print HELP
    sys.exit(1)
  return


if __name__ == '__main__':
  Main()
  # for f in GetSupportedFiles([sys.argv[1]]):
  #   print f
