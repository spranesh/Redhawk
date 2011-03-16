import util

import pprint
import yaml

FILES = [("_node_cfg.yaml", "_node.py", "_node_header.py")
#       ,("_type_cfg.yaml", "_type.py", "_type_header.py")
        ]

def GetClasses(file_body):
  """ Get a generator of classes, given the string of the body.
      This function guarantees that each class returned has the following
      attributes:
        * string
        * args
        * children
        * xml
        * json
        * dot
        * optargs
        * docstring
      All attributes except the docstring is a list."""
        
  nodes = yaml.load(file_body).items()
  nodes.sort()
  for (name, c) in nodes:
    util.AssertWithError(c.has_key('sexp'), "%s does not have string"%name)
    util.AssertWithError(c.has_key('args'), "%s does not have args"%name)

    default_fields = {'docstring' : 'Represents a %s construct'%name
                     ,'children' : ''
                     ,'optargs' : ''
                     ,'super': 'Node'
                     ,'xml' : None 
                     ,'json': None 
                     ,'dot':  None }
              
    default_fields.update(c)
    c = default_fields

    for m in "args children optargs".split():
      if c[m] == '':
        c[m] = []
      else:
        c[m] = c[m].split(", ")

    # pprint.pprint((name, c))
    yield (name, c)

def WriteMethodDeclaration(c, name, args, optargs):
  """ Write a method declaration:
    def name(self, args, optargs):
    in `c`"""
  # Function Definition
  c.Write("def %s(self"%(name))
  for a in args:
    c.Write(", %s"%a)
  for a in optargs:
    c.Write(", %s = None"%a)
  c.Write("):")
  c.NewLine()
  return


def WriteList(c, li, prefix=None):
  """ Write a list in `c`"""
  if prefix:
    li2 = [prefix + x for x in li]
  c.Write("[")
  c.Write(", ".join(li))
  c.Write("]")
  return


def WriteSExpMethod(c, name, li, args):
  """ Write the SExp method into `c`."""
  WriteMethodDeclaration(c, name, [], [])
  c.Indent()
  c.WriteLine("li = []")
  for a in li:
    if type(a) is str:
      if a in args:
        c.WriteLine("li.append(self.%s)"%(a))
      else:
        c.WriteLine("li.append('%s')"%(a))

    elif type(a) is list:
      if a[0][0] is '_':
        c.WriteLine("if %s:"%(a[0][1:]))
        c.Indent()
        c.Write("li.append(")
        WriteList(c, ["':%s'"%a[0][1:]] + a[1:], prefix='self.')
        c.Write(")")
        c.NewLine()
        c.Dedent()
      else:
        c.Write("li.append(")
        WriteList(c, a)
        c.Write(")")
        c.NewLine()
  
  c.WriteLine("return li")
  c.Dedent()
  c.NewLine()


def WriteAttributeMethod(c, name, li, args):
  """ Write the XML, JSON or Dot Methods into `c`."""
  WriteMethodDeclaration(c, name, [], [])
  c.Indent()
  c.WriteLine("d = {}")
  c.WriteLine("d['tags'] = []")
  for x in li:
    if x in args:
      c.WriteLine("d[%s] = self.%s"%(x, x))
    else:
      c.WriteLine("d['tags'].append('%s')"%(x))
  c.WriteLine("return (self.__class__.__name__, d)")
  c.Dedent()
  c.NewLine()
  return


def GenerateClass(name, attrs):
  c = util.CodeGeneratorBackend()
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


  # Write GetChildren
  WriteMethodDeclaration(c, "GetChildren", [], [])
  c.Indent()
  c.Write("return ")
  WriteList(c, attrs['children'], prefix='self.')
  c.NewLine()
  c.Dedent()
  c.NewLine()

  WriteSExpMethod(c, 'GetSExp', attrs['sexp'], args)

  if attrs['xml']:
    WriteAttributeMethod(c, 'GetXMLAttributes', attrs['xml'], args)

  if attrs['json']:
    WriteAttributeMethod(c, 'GetJSONAttributes', attrs['json'], args)

  if attrs['json']:
    WriteAttributeMethod(c, 'GetDotAttributes', attrs['dot'], args)
  c.Dedent()
  c.NewLine()

  c.GetCode()
  return c.GetCode()


def GetYAMLFileAsPythonCode(filename):
  """ Return the YAML file as a string of Python Code."""
  return "\n".join(
      map(lambda a: GenerateClass(a[0], a[1]),
        GetClasses(open(filename).read())))


def Main():
  for (ip_file, op_file, header_file) in FILES:
    print(ip_file, op_file, header_file)
    op = open(op_file, "w")
    op.write(open(header_file).read())
    op.write("\n")
    op.write(GetYAMLFileAsPythonCode(ip_file))
  return 0

if __name__ == '__main__':
  Main()
