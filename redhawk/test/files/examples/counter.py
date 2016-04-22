def CounterClosure(init=0):
  value = [init]
  def Inc():
    value[0] += 1
    return value[0]
  return Inc

class CounterClass:
  def __init__(self, init=0):
    self.value = init

  def Bump(self):
    self.value += 1
    return self.value

def CounterIter(init = 0):
  while True:
    init += 1
    yield init

if __name__ == '__main__':
  c1 = CounterClosure()
  c2 = CounterClass()
  c3 = CounterIter()
  assert(c1() == c2.Bump() == next(c3))
  assert(c1() == c2.Bump() == next(c3))
  assert(c1() == c2.Bump() == next(c3))
  
