
static int a_static_variable;

/* Some comments here on line numbers 4
 * and 5 */

int function_f(float f, char * str) 
{
  f *= 2;
  *str = 'c';
}

int main()
{
  int x = 7, y = 6, z = 5;

  float q = x * y - z + x * z;

  function_f(q, NULL);
  return;
}

