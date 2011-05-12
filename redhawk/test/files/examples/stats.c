/* Mean, and Variance of an array */
#include<stdlib.h>
#include<stdio.h>

float Mean(float *p, int len)
{
  float sum = 0;
  int i;

  for (i = 0; i < len; i++)
    sum += p[i];

  return sum/len;
}


float Variance(float *p, int len)
{
  /* Calculate Variance using E[X^2] - (E[X])^2 */
  float *q = malloc(sizeof(float) * len);
  float variance, mean_p, mean_q;
  int i;

  for(i = 0; i < len; i++)
    q[i] = p[i]*p[i];

  mean_p = Mean(p, len);
  mean_q = Mean(q, len);

  free(q);
  return mean_q - mean_p * mean_p;
}

int main()
{
  float a[] = {1, 2, 3, 4, 5};

  printf("Mean(a) = %f\n", Mean(a, 5));
  printf("Variance(a) = %f\n", Variance(a, 5));
  return;
}
