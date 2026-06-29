#include "my_revstr.h"

int my_strlen(char const str[])
{
	int count = 0;
	int i = 0;

	while (str[i] != '\0')
    	{
        	count += 1;
        	i += 1;
    	}
    	return count;
}

void my_revstr(char str[])
{
	int len = my_strlen(str);
    	int index = 0;
    	int end = len - 1;
    	char temporary;

    	while (index < end) 
	{
        temporary = str[index];
        str[index] = str[end];
        str[end] = temporary;

        index += 1;
        end -= 1;
    	}
}

