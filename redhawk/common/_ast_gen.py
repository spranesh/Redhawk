from __future__ import absolute_import
from __future__ import print_function
import redhawk.utils.util as U
import redhawk.utils.code_generator_backend as C

import pprint
import yaml
from six.moves import zip

FILES = [# (input config file, out file, header file)
           ("_node_cfg.yaml", "node.py", "_node_header.py")
          ,("_types_cfg.yaml", "types.py", "_types_header.py")]

def GetClasses(file_body):
  """ Get a generator of classes, given the string of the body.
      This function guarantees that each class returned has the following
      attributes:
        * sexp
        * args
        * children
        * xml
        * json
        * dot
        * optargs
        * docstring
      All attributes except the docstring is a list.
  """
  nodes = list(yaml.load(file_body).items())
  nodes.sort()

  for (name, c) in nodes:
    U.AssertWithError('sexp' in c, "%s does not have sexp"%name)

    # Print appropriate warnings
    for w_key in "docstring args children".split():
      if w_key not in c:
        U.LogWarning('%s does not have %s'%(name, w_key))


    default_fields = {'docstring' : 'Represents a %s construct'%name
                     ,'args': ''
                     ,'children' : ''
                     ,'optargs' : ''
                     ,'super': 'Node'
                     ,'xml' : None 
                     ,'json': None 
                     ,'dot':  None }
              
    default_fields.update(c)
    c = default_fields

    for m in "args children optargs".split():
      if c[m] == None:
        c[m] = None
      elif c[m] == '':
        c[m] = []
      else:
        c[m] = c[m].split(", ")

    # pprint.pprint((name, c))
    yield (name, c)


def WriteMethodDeclaration(c, name, args, optargs):
  """ Write a method declaration:
    def name(self, args, optargs):
    in c """
  # Function Definition
  c.Write("def %s(self"%(name))
  for a in args:
    c.Write(", %s"%a)
  for a in optargs:
    c.Write(", %s = None"%a)
  c.Write("):")
  c.NewLine()
  return


def WriteList(c, li, prefix=None, frame=None, start_of_list=None):
  """ Write a list, li, into c.

      1) Add the Prefix prefix to every element of the list that is a
         variable (and present in the frame).
      2) Depending on whether the element is in the frame or not,
         add the string or the variable.
      3) Add start_of_list to the start of the list without making
      any modifications.
  """

  start_of_list = start_of_list or []
  prefix = prefix or ''

  elements = []
  for x in li:
    if (not frame) or (frame and x in frame):
        elements.append(prefix + x)
    else:
      elements.append("'%s'"%(x))

  c.Write("[")
  c.Write(", ".join(start_of_list + elements))
  c.Write("]")
  return


def WriteListReturnMethod(c, name, li, args):
  """ Write methods that return lists.
      The sexp type lists given can only be nested upto a depth
      of 2."""
  WriteMethodDeclaration(c, name, [], [])

  # If there is only one variable, and it starts with a *
  if len(li) == 1 and li[0][0] == '*':
    c.Indent()
    c.WriteLine("return self.%s[:]"%(li[0][1:]))
    c.Dedent()
    c.NewLine()
    return

  c.Indent()
  c.WriteLine("li = []")

  for a in li:
    if type(a) is str:

      # If a starts and ends with backquotes, we copy it verbatim.
      if a[0] == '`':
        U.AssertWithError(a[-1] == '`', "No closing backquote found at %s"%a)
        c.WriteLine("li.append(%s)"%(a[1:-1]))

      # Otherwise, we check to see if it begins with a '*', and take
      # appropriate action
      else:
        method, value = "append", a
        if a[0] == '*':
          method, value = "extend", a[1:]
        if value in args:
          c.WriteLine("li.%s(self.%s)"%(method, value))
        else:
          c.WriteLine("li.%s('%s')"%(method, value))

    elif type(a) is list:
      # If the first letter of the first variable is an underscore (a condition)
      # we write:
      # if self.condition:
      #   li.append(['a[1]', rest of list])
      if a[0][0] is '_':
        condition = a[0][1:]
        U.AssertWithError(condition in args, "%s not in %s, %s, %s"%(condition,
          name, li, args))

        c.WriteLine("if self.%s:"%(condition))
        c.Indent()
        if len(a) == 2 and a[1][0] == '*':
          extend_list = a[1][1:]
          assert(extend_list in args)
          c.Write("li.append([':%s'] + self.%s)"%(extend_list, extend_list))
        else:
          c.Write("li.append(")
          WriteList(c, a[1:], 
              prefix='self.', 
              frame=args, 
              start_of_list=["'%s'"%(':' + condition)])
          c.Write(")")
        c.NewLine()
        c.Dedent()
      else:
        c.Write("li.append(")
        WriteList(c, a, prefix="self.", frame=args)
        c.Write(")")
        c.NewLine()
  
  c.WriteLine("return li")
  c.Dedent()
  c.NewLine()
  return


def WriteAttributeMethod(c, name, li, args):
  """ Write the XML, JSON or Dot Methods into `c`."""
  WriteMethodDeclaration(c, name, [], [])
  c.Indent()
  c.WriteLine("d = {}")
  # c.WriteLine("d['tags'] = []")
  for x in li:
    if x in args:
      c.WriteLine("d[%s] = self.%s"%(x, x))
    # else:
    #   c.WriteLine("d['tags'].append('%s')"%(x))
  c.WriteLine("return (self.__class__.__name__, d)")
  c.Dedent()
  c.NewLine()
  return


def GenerateClass(name, attrs):
  """ Generate class `name` given attributes `attrs`."""
  c = C.CodeGeneratorBackend()
  c.WriteLine("class %s(%s):"%(name, attrs['super']))
  c.Indent()
  c.WriteLine('"""%s"""'%(attrs['docstring']))

  # Write __init__
  WriteMethodDeclaration(c, '__init__', attrs['args'], attrs['optargs'])
  c.Indent()

  args = attrs['args'] + attrs['optargs']
  for x in args:
    c.WriteLine("self.%s = %s"%(x, x))
  c.WriteLine("return")
  c.Dedent()
  c.NewLine()

  if attrs['children']:
    WriteListReturnMethod(c, 'GetChildren', attrs['children'], args)

  WriteListReturnMethod(c, 'GetSExp', attrs['sexp'], args)

  attribute_list = "xml json dot".split()
  function_list = "GetXMLAttributes GetJSONAttributes, GetDotAttributes".split()
  for (a, f) in zip(attribute_list, function_list):
    if attrs[a]:
      WriteAttributeMethod(c, f, attrs[a], args)

  c.Dedent()
  c.NewLine()

  return c.GetCode()


def GetYAMLFileAsPythonCode(filename):
  """ Return the YAML file as a string of Python Code."""
  return "\n".join(
      [GenerateClass(a[0], a[1]) for a in GetClasses(open(filename).read())])


def Main():
  for (ip_file, op_file, header_file) in FILES:
    print((ip_file, op_file, header_file))
    op = open(op_file, "w")
    op.write(open(header_file).read())
    op.write("\n")
    op.write(GetYAMLFileAsPythonCode(ip_file))
  return 0

if __name__ == '__main__':
  Main()
