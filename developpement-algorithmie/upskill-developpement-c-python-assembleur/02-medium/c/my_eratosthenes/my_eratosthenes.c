#include <stdio.h>
#include "my_eratosthenes.h"

void my_eratosthenes(int n) 
{
	if (n > 1000) 
	{										// N ne peut pas être supérieur à 1000
		return;
    }

	int result_table[n + 1];				// On crée un tableau qui contient le résultat
	int i = 0;

	while (i <= n)							// Tant que le nombre ne dépasse pas la taille du tableau
	{
		result_table[i] = 1;		  		// On définit tous les nombres comme premiers
        i += 1;
    }

        i = 2;  							// 0 et 1 ne sont pas premiers, donc on commence à 2
						
	while (i <= n)	 						
	{						
		if (result_table[i] == 1)			// Si i est marqué comme étant premier
		{  						
			int j = 2 * i;	 	 				
            while (j <= n) 
			{
            	result_table[j] = 0;		// Marquer j comme non-premier
                j += i;		     		
            }
        }
        i += 1;
    }	

        i = 2;  							// Les nombres premiers commencent à 2 donc i n'affichera
    while (i <= n) 							// ni 0, ni 1.
	{
     	if (result_table[i] == 1) 			// Si i est marqué comme étant premier
		{ 
           	 printf("%d\n", i);  			// Afficher i
        }
        i += 1;
    }
}
