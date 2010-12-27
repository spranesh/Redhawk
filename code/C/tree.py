# Definition of the parse tree
import sys

def ListToString(l):
  return "[" + " ".join(map(str, l)) + "]"

class Position:
  def __init__(self, file, row, col):
    self.file = file
    self.row = row
    self.col = col

  def __repr__(self):
    return "[%s] %d:%d"%(self.file, self.row, self.col)

class Tree:
  def __init__(self, node_type, position, name=""):
    self.type = node_type
    self.position = position
    self.name = name
    self.children = []
    self.attributes = {}
    self.tags = []
  
  def AddAttributes(self, key, value):
    self.attributes[key] = value

  def AddTag(self, tag):
    self.tags.append(tag)
  
  def AddChild(self, tree):
    self.children.append(tree)

  def ShowThisNode(self, fp=sys.stdout, prefix=""):
    fp.write(prefix)
    fp.write("'%s %s %s"%(self.type, self.name, self.position))
    fp.write("\n" + prefix)
    fp.write("tags : " + ListToString(self.tags))
    fp.write("\n" + prefix)
    fp.write("attributes : " + ListToString(self.attributes.items()))

class Declaration(Tree):
  def __init__(self, name, position):
    Tree.__init__(self, 'decl', position, name)

Declaration('haha', Position('file.c', 2, 5)).ShowThisNode()

