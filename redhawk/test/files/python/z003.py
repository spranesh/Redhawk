# Test Break and Continue

from __future__ import absolute_import
from six.moves import range
for i in range(100):
  if i*i%100 == 0:
    break
  else:
    continue
