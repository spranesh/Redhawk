# Test Statements
from __future__ import print_function
from __future__ import absolute_import
from six.moves import range
a = b + c
(a, b) = b, a+b
b += 1
c *= 100
for i in range(100): sum+=i*2
while i < 100: i += 1
assert(True == True)
assert(True != False, "Python doesn't understand True and False!")
del li
del li[2]
print(a)
print(a, b, c)
print(a, b, c, file=sys.stderr)
def f(a): pass
raise AttributeError("Oh noes! Attribute Error!")
global x, y
exec(2 + 3)
