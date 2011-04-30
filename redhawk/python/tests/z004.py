# Test Try, Except

try:
  x = a.x
  y = a.y
  z = a.array[0]
except AttributeError, e:
  x = 1
  y = 1
  z = 1
except IndexError, e:
  x = 0
  y = 0
  z = 0
