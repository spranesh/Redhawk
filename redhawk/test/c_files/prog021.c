// GOTO

int foo()
{
  int a = 1;
  while(a < 10) {
    if(a == 5)
      goto end;
    a = f(a);
  }

  printf(a);

end: 
  a *= 2;
  return a;
}


