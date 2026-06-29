#include "my_utf8_count_char.h"

int my_utf8_count_char(const char *str)
{
	int count = 0;

	while (*str != '\0') 
	{
        	if ((*str & 0x80) == 0) 		// Comparaison bit à bit de la valeur de str avec 0x80 
		{					// (1000 0000 en binaire) pour isoler le 1er bit
							// si le bit le plus à gauche est à 0, le caractère est un ASCII 
							// (codé sur 1 octet) car ces caractères vont de 0 à 127
							// Voir wikipedia utf8
		
            		count += 1;
            		str += 1;			// On se décale d'un octet
        	}
       		 else if ((*str & 0xE0) == 0xC0) 	// Comparaison bit à bit avec 0xE0 (1110 0000) pour isoler les 2 1er bit
							// si les 2 bit à gauch sont à 1, le caractère est codé sur 2 octets
		{
            		count += 1;
            		str += 2;			// On se décale de 2 octets
        	}
        	else if ((*str & 0xF0) == 0xE0) 	// Comparaison bit à bit avec 0xF0 (1111 0000) pour isoler les 3 1er bit
							// si les 3 bit à gauche sont à 1, le caractère est codé sur 3 octets
		{
            		count += 1;
           		 str += 3;			// On se décale de 3 octets
        	}
        	else if ((*str & 0xF8) == 0xF0) 	// Comparaison bit à bit avec 0xF8 (1111 1000) pour isoler le 1er bit
							// si les 4 bits à gauche sont à 1, le caractère est codé sur 4 octets
		{
            		count += 1;
            		str += 4;			// On se décale de 4 octets sur la chaîne
        	}
        	else {
            		str += 1;
        	}
    	}	
	return count;
}

