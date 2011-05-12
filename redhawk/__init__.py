import os

__version__ = '1.1.0dev'
DB_NAME = '.redhawk_db'

def GetVersion():
  return __version__

def GetDBName():
  return DB_NAME
