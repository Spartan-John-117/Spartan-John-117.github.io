#include <stdio.h>

long int my_sum(long int a1, long int a2, long int a3,
                 long int a4, long int a5,
                 long int a6, long int a7);

int main() {
    long int result;


    result = my_sum(1, 2, 3, 4, 5, 6, 7);
    

    printf("La somme est : %ld\n", result);

    return 0;
}

