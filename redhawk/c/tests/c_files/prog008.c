int f(int a)
{
  return a + 3;
}

int main()
{
  (*g)(3);
  return f(2);
}
