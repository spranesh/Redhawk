int IsLeapYear(unsigned int year)
{
  if(year%400 == 0) {
    return 0;
  } else if(year%4 == 0) {
    return 1;
  } else {
    return 0;
  }
}
    

