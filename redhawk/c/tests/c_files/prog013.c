int Factorial(int n)
{
  int fact = 1;
  int m = 1;

  do {
    fact *= m;
    m++;
  } while(m < n);

  return m;
}

