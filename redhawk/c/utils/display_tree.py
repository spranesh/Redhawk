#!/usr/bin env python

import sys
import pycparser

def GetNodeTypeShorthand(node):
  cparser_type = ""
  if hasattr(node, 'type'):
    cparser_type = str(node.type).split(' ')[0].rsplit('.')[-1]
  # python_type = str(type(node)).split('.')[-1][:-2]  
  python_type = node.__class__.__name__
  if python_type and cparser_type:
    return "p%s-c%s"%(python_type, cparser_type)
  if python_type:
    return "p"+python_type
  return "c"+cparser_type

def GetNodeName(node):
  name = ''
  while hasattr(node, 'name'):
    name = node.name
    node = node.name
  return name


def NodeToString(node):
  if node.coord:
    position = '[%s] %d:%d'%(
      node.coord.file or '', 
      node.coord.line or 0,
      node.coord.column or 0)
  else:
    position = '[] 0:0'

  name = GetNodeName(node)
  if name:
    name = " '" + name

  return "%s%s"%(str(GetNodeTypeShorthand(node)).lower(), name)

def PrintTree(tree, indent_level = 0, fp=sys.stdout):

  fp.write("\n%s(%s"%(' '*indent_level, NodeToString(tree)))
  if len(tree.children()) == 0:
    fp.write(")")
  else:
    #fp.write("\n")
    for c in tree.children():
      PrintTree(c, indent_level+2)
    fp.write(")")

try:
  filename = sys.argv[1]
except IndexError, e:
  sys.stderr.write("No C file specified to parse.\n")
  sys.exit(1)

#tree = pycparser.parse_file(filename)
tree = pycparser.parse_file(filename, use_cpp = True, cpp_path='cpp', cpp_args='-Ifake_libc_include')

#tree.show(attrnames=True, showcoord=True)
PrintTree(tree)

