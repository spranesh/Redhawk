""" The Node Class. """

import copy

class Node:
  """ Signifies a node in the parse tree."""
  def __init__(self, 
      type, 
      properties=None, 
      children=None, 
      tags=None, 
      position=None):

    if properties is None: properties = {}
    if tags is None: tags = []
    if children is None: children = []
    self.type = type
    self.properties = properties
    self.children = children
    self.tags = tags
    self.position = position
    return

  def __repr__(self):
    return self.ConvertToString()

  def __repr__(self):
    return self.ConvertToString()

  def GetChildren(self):
    return self.children

  def GetCopy(self):
    return copy.deepcopy(self)

  def GetPosition(self):
    return self.position

  def GetProperty(self, key):
    return self.properties[key]

  def GetProperties(self):
    return self.properties

  def GetTags(self):
    return self.tags

  def GetType(self):
    return self.type

  def AddChild(self, n):
    self.children.append(n)
    return

  def AddChildren(self, li):
    for n in li:
      self.AddChild(n)
    return

  def AddProperty(self, attr, value):
    self.properties[attr] = value
    return

  def AddPropertiesFrom(self, obj, attrs):
    for attr in attrs:
      self.AddProperty(attr, getattr(obj, attr))

  def AddTag(self, tag):
    self.tags.append(tag)
    return

  def AddTags(self, tags):
    for tag in tags:
      self.tags.append(tag)
    return

  def ConvertToString(self, leading_whitespace=0):
    s = " "*leading_whitespace
    s += "(" + self.type + " "
    if self.properties.has_key('name'):
      s += self.properties['name'] + " "
    s += "'("
    for p in self.properties:
      if p in "type storage".split():
        s += "(%s %s)"%(p, self.properties[p])
    s += ")"

    for c in self.children:
      s+="\n"
      s+=c.ConvertToString(leading_whitespace+2)
    s+=")"
    return s

