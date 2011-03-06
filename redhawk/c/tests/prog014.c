int isspace(char c)
{
  int temp = 0;
  switch(c)
  {
    case ' ': 
    case '\t':
    case '\n':
      temp = 1; // DEBUG
      return 1;
    default:
      return 0;
  }

}
