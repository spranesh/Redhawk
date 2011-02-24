#!/usr/bin/env python
import node
import node_position

class TestNode:
  def __init__(self):
    return

  def setUp(self):
    self.n = node.Node('define-function')

    self.p = node.Node('define-function', 
        properties={'name': 'f'}, 
        children=[],
        tags=["scope"], 
        position=node_position.NodePosition('a', 10, 20))

    self.q = node.Node('define-variable', 
        properties={'name': 'f'}, children=[],
        tags=[])
    return

  def TestInit(self):
    assert(self.n!=None)
    return

  def TestGetAttributes(self):
    assert(self.p.GetType() == 'define-function')
    assert(self.p.GetProperties() == {'name' : 'f'})
    assert(self.p.GetProperty('name') == 'f')
    assert(self.p.GetChildren() == [])
    assert(self.p.GetTags() == ["scope"])

    assert(self.p.GetPosition().GetFile() == "a")
    assert(self.p.GetPosition().GetLine() == 10)
    assert(self.p.GetPosition().GetColumn() == 20)
    return

  def TestAddChildren(self):
    assert(self.q not in self.p.GetChildren())
    self.p.AddChild(self.q)
    assert(self.q in self.p.GetChildren())

    assert(self.n not in self.p.GetChildren())
    assert(self.p not in self.p.GetChildren())
    self.p.AddChildren([self.n, self.p])
    assert(self.n in self.p.GetChildren())
    assert(self.p in self.p.GetChildren())

    # Also test order
    assert(self.p.GetChildren()[-2:] == [self.n, self.p])
    return

  def TestAddProperty(self):
    assert(self.p.GetProperties().has_key('asdf') == False)
    self.p.AddProperty('asdf', 1234)
    assert(self.p.GetProperties().has_key('asdf') == True)
    assert(self.p.GetProperties()['asdf'] == 1234)
    return

  def TestAddPropertiesFrom(self):
    # Define a simple structure class
    class Boo:
      def __init__(self, name, type, foo):
        self.name = name
        self.type = type
        self.foo = foo

    obj = Boo('main', 'blah', 'bar')

    # Name already exists, so check the others.
    assert('type' not in self.p.GetProperties())
    assert('foo' not in self.p.GetProperties())
    self.p.AddPropertiesFrom(obj, ['name', 'type', 'foo'])
    assert(self.p.GetProperty('name') == 'main')
    assert(self.p.GetProperty('type') == 'blah')
    assert(self.p.GetProperty('foo') == 'bar')
    return

  def TestAddTags(self):
    assert("blah" not in self.p.GetTags())
    self.p.AddTag("blah")
    assert("blah" in self.p.GetTags())

    assert("foo" not in self.p.GetTags())
    assert("bar" not in self.p.GetTags())
    self.p.AddTags(["foo", "bar"])
    assert("foo" in self.p.GetTags())
    assert("bar" in self.p.GetTags())
    return

