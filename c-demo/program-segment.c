#include <stdio.h>

int numval;

int main() {
  printf("How many values?\n");
  scanf("%d", &numval);

  int loop_counter;
  int value;
  int result = 0;

  for (loop_counter = 0; loop_counter < numval; loop_counter++) {
    result = result + loop_counter;
  }

  printf("Result = %d\n", result);
  return result;
}
