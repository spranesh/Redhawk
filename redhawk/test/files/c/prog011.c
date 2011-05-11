// Iterative Fibonacci
int Fibonacci(int n)
{
  int a = 1, b = 1;
  int i, temp;

  if(n == 0 || n == 1)
    return 1;

  // Loop should run for n - 2 times
  for(i = 0; i < n - 2; i++) {
    temp = b;
    a += b;
    b = temp;
  }
  return a;
}


