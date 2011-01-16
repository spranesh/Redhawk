
int Fib(int n)
{
  if(n < 0)
    assert(false);

  if(n == 0)
    return 0;
  else if (n == 1)
    return 1;
  else
    return Fib(n-1) + Fib(n-2);
}

void ShowFib(int n)
{
  int i;
  for(i = 0; i < n; i++)
    printf("%d\n", Fib(i));
  return;
}
