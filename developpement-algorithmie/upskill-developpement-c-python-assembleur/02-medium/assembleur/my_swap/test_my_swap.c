#include <stdio.h>

void my_swap(long int *nbr1, long int *nbr2);

int main() {
    long int a = 42;
    long int b = 84;

    printf("Avant l'échange : a = %ld, b = %ld\n", a, b);

    my_swap(&a, &b);

    printf("Après l'échange : a = %ld, b = %ld\n", a, b);

    return 0;
}
