#include <stdio.h>

unsigned long long factorial(unsigned long long x) {
  if (x < 2L) {
    return 1L;
  }
  return x * factorial(x - 1L);
}

long long catalan_number(long long x) {
  return factorial(2L * x) / (factorial(x + 1L) * factorial(x));
}

long long number_of_attempts(long long x) {
  return (3L * x - 2L) * catalan_number(x - 1L);
}

long long possible_solutions(long long x) {
  if (x == 1L) {
    return 1L;
  }
  return possible_solutions(x - 1L) + number_of_attempts(x - 1L);
}

int main(void) {
  printf("starting\n");
  printf("\nSolutions: %lld", possible_solutions(3L));
  printf("\nDone\n");

  return 0;
}
