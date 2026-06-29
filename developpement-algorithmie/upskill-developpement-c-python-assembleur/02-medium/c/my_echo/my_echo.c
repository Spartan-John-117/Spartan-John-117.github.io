#include "my_echo.h"			// On importe les dépendance pour que le fichier y accède
#include "my_putchar.h"

void my_echo(char const str[]) 
{
	int i = 0;			// On initialise l'index à 0
	while (str[i] != '\0') 		// Tant que la valeur de str[i] n'est pas null
{
		my_putchar(str[i]);	// On appelle la fonction my_putchar pour traiter un caractère l'emplacement i
		i += 1;			// On incrément i de 1
}
	my_putchar('\n');		// On ajoute un retour à la ligne
}
