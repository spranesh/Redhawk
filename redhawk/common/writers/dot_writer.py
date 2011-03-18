#!/usr/bin/env python

import redhawk.common.node as N
import redhawk.common.utils.misc_utils as U
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

# node [ shape=box, color=gray, fontname="Sans", fontsize=10 ]
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
    label += ["%s: %s"%(k, v) for (k, v) in attrs.items() if type(v) is str]

    return self.__CreateGraphNode(label = ", ".join(label))


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

    for child in ast_node.GetChildren():

      if type(child) is list:
        empty_node = self.__CreateEmptyGraphNode()
        self.graph.add_edge(node_index, empty_node)
        map(lambda a: self.AddASTNodeToGraph(empty_node, a),
              child)
      elif isinstance(child, N.Node):
        self.AddASTNodeToGraph(node_index, child)

      elif type(child) is type(None):
        continue

      else:
        U.AssertWithError(False, 
          "%s's child (type: %s) was supposed to be a Node!\n %s"
          %(ast_node.GetName(),
            type(child),
            ast_node))

    return

