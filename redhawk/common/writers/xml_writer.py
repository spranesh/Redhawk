#!/usr/bin/env python

""" Implementation of the XML Writer"""

from __future__ import absolute_import
from __future__ import print_function
import redhawk.common.node as N
import redhawk.common.type as T
import redhawk.utils.util as U
from . import writer

import lxml.etree as ET

def WriteToXML(tree):
  s = XMLWriter()
  return s.WriteTree(tree)


def WriteToFile(tree, filename):
  s = XMLWriter()
  s.GetTree(tree).write(filename)
  return


class XMLWriter(writer.Writer):
  def __init__(self):
    return

  def __AddChildToElement(self, child, parent_element):
    """ Adds a Child (which could itself be a list) as a child to the
    parent_element."""
    if  type(child) is list:
      group_node = ET.SubElement(parent_element, "ChildGroup")
      for c in child:
        self.__AddChildToElement(c, group_node)
    else:
      assert(isinstance(child, N.Node) or child == None)
      if child == None:
        print("We have a none child?")
        ET.SubElement(parent_element, "None")
      else:
        self.__ConvertToElement(child, parent_element)
    return

  def __AddPositionToElement(self, tree, parent_element):
    try:
      line, column, f = tree.position.GetLine(), tree.position.GetColumn(), tree.position.GetFile()
    except AttributeError as e:
      line, column, f = None, None, None

    attributes = {
        'line'    : str(line),
        'column'  : str(column),
        'file'    : str(f)
    }
    
    position_element = ET.SubElement(parent_element, "Position", attrib=attributes)
    return

  def __ConvertToElement(self, tree, parent_element):
    """ Converts a tree to an element tree, whose parent is `parent_element`."""
    attributes = dict([(key, val) for (key, val) 
      in tree.GetXMLAttributes()[1].items() if type(val) is str])

    print(attributes)
    print(tree.GetName())
    node_element = ET.SubElement(parent_element, tree.GetName(), attrib=attributes)
    self.__AddPositionToElement(tree, node_element)
    self.__AddChildToElement(tree.GetChildren(), node_element)
    return


  def WriteTree(self, tree):
    """ Implementation of the base class method for writing the tree to a
        string."""
    return ET.tostring(self.GetTree(tree))

  def GetTree(self, tree):
    root = ET.Element("last")
    self.__ConvertToElement(tree, root)
    tree = ET.ElementTree(root)
    return tree
