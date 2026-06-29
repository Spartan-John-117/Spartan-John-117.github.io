#include "my_get_nbr.h"

int my_get_nbr(char const str[])
{
        int i = 0;						// On initialise i (index) à 0
	int nombre = 0;						// On initialise nombre (le résultat) à 0
	int signe = 1;						// Dans le cas où le nombre serait négatif on crée
								// une variable pour récupérer le signe (+ ou -)

	if (str[i] == '-')					// Si premier caractère est un (-)
	{
		signe = -1;					// Le signe passe à -1 (voir l'utilité plus loin)
		i += 1;						// On incrémente l'index de 1
	}

        while (str[i] != '\0')					// Notre boucle se poursuite tant que le caractère
								// en cours n'est pas null
	{
		if (str[i] >= '0' && str[i] <= '9')		// Si le la valeur de str[i] est comprise en 0 et 9
		{
			int chiffre = str[i] - '0';		// On soustrait la valeur de 0 à la valeur de str[i]
								// exemple : valeur de str[i] = 9 (39 en hexa)
								// 9 (39 en hexa) - 0 (30 en hexa) = 9
			nombre = nombre * 10 + chiffre;		// Pour obtenir le nombre on multiplie le nombre
								// précédemment obtenu par 10, et on ajouter le chiffre
		}
	
		i += 1;	
	}
	return nombre * signe;
}
