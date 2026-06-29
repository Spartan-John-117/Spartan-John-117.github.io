#include "my_sort.h"

void my_sort(int arr[], unsigned int length) {                
    for (unsigned int i = 0; i < length - 1; ++i) {             // Tri par sélection
        unsigned int min_index = i;
                                                  
        for (unsigned int j = i + 1; j < length; ++j) {         // Trouver l'indice de l'élément minimum dans
            if (arr[j] < arr[min_index]) {                      // le sous-tableau non trié
                min_index = j;
            }
        }                                             
        if (min_index != i) {                                   // Si l'élément minimum n'est pas déjà à sa place,
            int temp = arr[i];                                  // on échange les éléments
            arr[i] = arr[min_index];
            arr[min_index] = temp;
        }
    }
}