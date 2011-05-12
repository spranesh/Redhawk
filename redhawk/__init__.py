import os

def GetVersion():
  fp = open(os.path.join(os.path.dirname(__file__), "VERSION"))
  version = fp.read().strip()
  fp.close()
  return version
