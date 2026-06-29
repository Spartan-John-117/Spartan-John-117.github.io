#include "my_hanoi.h"
#include <stdio.h>

void print_move(int origin, int destination) 										// Création d'une fonction utilisant putchar
{																					// pour afficher les déplacements
	putchar('0' + origin);															// Pour afficher un int avec la fonction putchar, il faut le convertir
	putchar('-');																	// en char en effectuant l'opération '0' + (de 1 à 9)
	putchar('>');
	putchar('0' + destination);
	putchar('\n');
}

void my_hanoi_recursive(unsigned n, int origin, int destination, int middle) 		// Création d'une fonction pour la récursivié qui prend 3 paramètres
{
	if (n == 1)																		// Si n == 1, déplacer un seul disque de origin à destination
	{
        print_move(origin, destination);
    	}
	else 
	{
        my_hanoi_recursive(n - 1, origin, middle, destination);						// Déplace le n-1 de origin vers middle
        print_move(origin, destination); 											// Affiche le déplacement du dernier disque vers la destination
        my_hanoi_recursive(n - 1, middle, destination, origin);						// Déplace le n-1 de middle vers destination
    	}
}

void my_hanoi(unsigned n)															// Appel de la fonction donnée 
{
    my_hanoi_recursive(n, 1, 3, 2);
}

