#include "my_nbr_digit.h"

int my_nbr_digit(int number, int base)
{
	if (number == 0)
        return 1;

	int counter = 0;

	while (number > 0)
	{
		number = number / base;
		counter += 1; 
	}
return counter;
}
