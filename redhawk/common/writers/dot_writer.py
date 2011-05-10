#!/usr/bin/env python

import redhawk.common.node as N
import redhawk.common.types as T
import redhawk.utils.util as U
import writer

import itertools
import pygraphviz

def WriteToDot(tree):
  s = DotWriter()
  return s.WriteTree(tree)


def WriteToImage(tree, fmt='png', filename=None):
  s = DotWriter()
  s.AddTree(tree)
  s.Draw(path=filename, fmt=fmt)
  return


def EscapeWhitespace(s):
  a = s.replace("\n", "\\\\n").replace("\t", "\\\\t")
  return a


class DotWriter(writer.Writer):
  def __init__(self):
    self.node_name_counter = itertools.count(0)
    self.graph = pygraphviz.AGraph(directed=True, rankdir='LR')
    self.graph.layout(prog='dot')
    return


  def WriteTree(self, tree):
    """ Implementation of the base class method for writing the tree to a
        string."""
    self.AddTree(tree)
    return self.graph.to_string()

  def Draw(self, path, fmt='png'):
    self.graph.draw(path=path, format=fmt, prog='dot')
    return

  def AddTree(self, tree):
    """ Adds the tree to the graph."""
    self.AddASTNodeToGraph(None, tree)
    return


  def __CreateGraphNode(self, **attrs):
    """ Create a graph node with the give attributes."""
    node_index = self.node_name_counter.next()
    self.graph.add_node(node_index, **attrs)
    return node_index
    

  def __CreateGraphNodeFromAST(self, ast_node):
    """ Create a Graph Node (with the relevant attributes) 
          from the ast_node
        Return the node index."""
    name, attrs = ast_node.GetDotAttributes() 
    label = [name]
    label += ["%s: %s"%(EscapeWhitespace(str(k)), EscapeWhitespace(str(v)))
      for (k, v) in attrs.items() if type(v) is str]

    if isinstance(ast_node, T.Type):
      color = "gray"
      fontcolor = "blue"
    else:
      color = "gray"
      fontcolor = "black"

    return self.__CreateGraphNode(label = ", ".join(label)
                                 ,shape = "box"
                                 ,color = color
                                 ,fontcolor = fontcolor
                                 ,fontname = "Sans"
                                 ,fontsize = "10")


  def __CreateEmptyGraphNode(self):
    """ Create an Empty Node (with style), and return its index."""
    return self.__CreateGraphNode(shape='circle', 
                                style='filled',
                                label="",
                                height='.1',
                                width='.1')


  def AddASTNodeToGraph(self, parent_index, ast_node):
    """ Creates a Graph Node from the given AST node,
        marks its parent as the graph node with the given
        `parent_index`, and recurses on the given AST
        node's children."""

    node_index = self.__CreateGraphNodeFromAST(ast_node)

    if parent_index is not None:
      self.graph.add_edge(parent_index, node_index)

    children = ast_node.GetChildren()
    types = [x for x in ast_node.GetAttributes()[1].values() if isinstance(x, T.Type)]
    children = types + children
    
    for child in children:
      if child is None:
        continue

      if type(child) is list:
        empty_node = self.__CreateEmptyGraphNode()
        self.graph.add_edge(node_index, empty_node)
        map(lambda a: self.AddASTNodeToGraph(empty_node, a),
              child)
      elif isinstance(child, N.Node):
        self.AddASTNodeToGraph(node_index, child)

      elif child is None:
        continue

      else:
        U.ExitWithError("%s's child (type: %s) was supposed to be a Node!\n %s"
          %(ast_node.GetName(),
            type(child),
            ast_node))

    return

