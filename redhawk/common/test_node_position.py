#!/usr/bin/env python

import node_position

class TestNodePosition:
  def __init__(self):
    return

  def setUp(self):
    self.a = node_position.NodePosition("a", 10, 20)
    return

  def TestInit(self):
    assert(self.a!=None)
    return

  def TestNodePositionGetAttributes(self):
    assert(self.a.GetFile() == "a")
    assert(self.a.GetLine() == 10)
    assert(self.a.GetColumn() == 20)
    return

