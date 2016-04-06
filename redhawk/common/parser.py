""" Parser base class for the various langauge implementations.

Various language implementations have to 
  a) provide the GetTreeConverterClass() method for their language.
  b) provide the Parse Method for their language.
 """

from __future__ import absolute_import
from . import tree_converter as T

class Parser:
  def GetTreeConverterClass(self):
    raise NotImplementedError(
      "GetTreeConverterClass method not implemented in the Parser base class.")

  def Parse(self, filename):
    """ Parse filename. """
    raise NotImplementedError(
      "Parse is not implemented in the Parser base class.")

  def _Get_Converter(self, filename):
    converter_class = self.GetTreeConverterClass()
    assert(issubclass(converter_class, T.TreeConverter))
    converter = converter_class(filename)
    return converter

  def Convert(self, ast, filename=None):
    """ Convert language specific AST to the LAST """
    return self._Get_Converter(filename).Convert(ast)

  def GetLAST(self, filename):
    """ Return the language agnostic abstract syntax tree for filename."""
    assert(filename != None)
    converter = self._Get_Converter(filename)
    return converter.Convert(self.Parse(filename))
