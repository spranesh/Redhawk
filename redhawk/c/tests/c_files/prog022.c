union sign   /* A definition and a declaration */
{
    int svar;
    unsigned uvar;
};


int main()
{
  union sign blah;
  blah.uvar = 56;
  return;
}
