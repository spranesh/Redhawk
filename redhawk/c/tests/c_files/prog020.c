// Test Break and Continue


int foo()
{
  a = 1;
  while(True) {
    a = f(a);

    if (a%2 == 0) {
      a /= 2;
      continue;
    }

    if (a == 1) {
      break;
    }
  }
  return a;
}




