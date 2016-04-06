# Test Try, Except

from __future__ import print_function
try:
  x = a.x
  y = a.y
  z = a.array[0]
except AttributeError as e:
  x = 1
  y = 1
  z = 1
except IndexError as e:
  x = 0
  y = 0
  z = 0
finally:
  print(x, y, z)
