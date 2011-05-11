# Test With Statement

f()
fopen(filename)
with fopen(filename) as fp:
  x = fp.readline()
  y = fp.readline()
  s = fp.read()

# Open and close a file.
with fopen(filename):
  pass

with (fopen(filename1), fopen(filename2)) as (fp1, fp2):
  pass
