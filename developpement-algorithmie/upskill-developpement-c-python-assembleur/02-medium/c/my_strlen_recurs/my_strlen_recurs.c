#include "my_strlen_recurs.h"

int my_strlen_recurs(char const str[])
{
	if (str[0] == '\0')				// Test qui permet de sortir de la récursivité
		return 0;				// si le caractère en cours est null

	return 1 + my_strlen_recurs(str + 1);		// Pour chaque itération de la récursivité, on compte 1
							// puis on passe le caractère suivant à la fonction my_strlen
}
