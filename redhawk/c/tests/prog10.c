int Fibonacci(int n)
{
  if(n == 0 || n == 1)
    return 1;

  else
    return Fibonacci(n-1) + Fibonacci(n-2);
}

