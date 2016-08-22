from __future__ import absolute_import
import os

__version__ = '1.2.2'
DB_NAME = '.redhawk_db'

def GetVersion():
  return __version__

def GetDBName():
  return DB_NAME
