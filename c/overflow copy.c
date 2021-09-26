#include <stdio.h>

unsigned long long factorial(unsigned long long x) {
  if (x < 2L) {
    return 1L;
  }
  return x * factorial(x - 1L);
}

void calculate_factorial(unsigned long long x) {
  printf("Factorial of %lld: %lld\n", x, factorial(x));
}

int main(void) {
  calculate_factorial(5L);
  calculate_factorial(20L);
  calculate_factorial(50L);
  calculate_factorial(80L);
  return 0;
}
