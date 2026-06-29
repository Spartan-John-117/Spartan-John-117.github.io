#include "my_alphabet.h"
#include <unistd.h>

int my_alphabet(void) {

		int i = 0;								
		int count = 0;						// Initialisation du compteur de lettres
		char letter = 0x61;					// Initialisation de la valeur de letter avec "a" en hexa

		for (i = 0; i < 26; i+=1)			// Boucle for en C (valeur de départ, valeur max, incrémentation)
		{
				write (1, &letter, 1);		// Affiche (sur le terminal, la lettre en cours, d'une longueur d'un octet
				count += 1;
				letter += 1;
		}
return count;								// Retourne count, sans l'afficher
}
