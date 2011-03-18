int Factorial(int n)
{
  int fact = 1;
  int m = 1;

  while(m <= n) {
    fact *= m;
    m++;
  }
  return m;
}

