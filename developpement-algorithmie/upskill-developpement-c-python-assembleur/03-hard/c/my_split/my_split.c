#include <stdlib.h>
#include <string.h>

char **my_split(const char * const str, const char * const sep)
{                                                                            
    int i, j, k;                                                                // Variables pour l'indexation
    int count = 1;                                                              // Compteur de sous-chaînes (initialisé à 1 
                                                                                // pour le cas où il n'y a pas de séparateur)
    int len = strlen(str);                                                      // Longueur de la chaîne d'entrée
                                                                            
    for (i = 0; i < len; i++) {                                                 // Compter le nombre de sous-chaînes créées 
        for (j = 0; sep[j] != '\0'; j++) {                                      // par les séparateurs
            if (str[i] == sep[j]) {
                count++;                                                        // Incrémente le compteur lorsqu'on rencontre 
                break;                                                          // un séparateur
            }
        }
    }                                                                          
    char **result = malloc((count + 1) * sizeof(char *));                       // Allouer un tableau pour contenir 
    if (result == NULL) {                                                       // les sous-chaînes
        return NULL;                                                            // Si l'allocation échoue, retourner NULL
    }
    int start = 0;                                                              // Variables de découpage
    int sub_str_idx = 0;

    for (i = 0; i <= len; i++) {                                                // Découper la chaîne `str` en sous-chaînes
        int is_separator = 0;                                                    
        for (j = 0; sep[j] != '\0'; j++) {                                      
            if (str[i] == sep[j] || str[i] == '\0') {                           // Vérifier si on rencontre un séparateur
                is_separator = 1;                                               // ou la fin de la chaîne
                break;
            }
        }
        if (is_separator || str[i] == '\0') {                                                             
            int sub_str_len = i - start + 1;                                    
            result[sub_str_idx] = malloc(sub_str_len * sizeof(char));           // Allouer de l'espace pour la sous-chaîne
                                                                                // longueur de la sous-chaîne
            if (result[sub_str_idx] == NULL) {                                  // Si l'allocation échoue, libérer tout ce                                                                    
                for (k = 0; k < sub_str_idx; k++) {                             // qui a été alloué
                    free(result[k]);
                }
                free(result);
                return NULL;
            }          
            strncpy(result[sub_str_idx], &str[start], sub_str_len - 1);          // Copier la sous-chaîne dans le tableau
            result[sub_str_idx][sub_str_len - 1] = '\0';                        // Terminer la chaîne

            start = i + 1;                                                      // Mettre à jour les variables pour la 
            sub_str_idx++;                                                      // prochaine sous-chaîne
        }
    }                                                                              
    result[sub_str_idx] = NULL;                                                 // Ajouter un pointeur NULL à la fin du tableau
    return result;
}
