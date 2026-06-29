#include "my_strlen.h"

int my_strlen(char const str[])
{
	int count = 0;			// Initialisation du compteur à 0
	int i = 0;			// Initialisation de l'index à 1 

	while (str[i] != '\0')		// La boucle continue tant que le caractère n'est pas null
	{
	count += 1;			// On incrémente le compteur de 1
	i += 1;				// On incrémente l'index de 1
	}	
	return count;

}
