""" Definition of the NodePosition class."""

class NodePosition:
  def __init__(self, file, line, column):
    self.file = file
    self.line = line
    self.column = column
    return

  def __repr__(self):
    return "[%s:%4d:%3d]"%(self.file, self.line, self.column)
  
  def __str__(self):
    return self.__repr__

