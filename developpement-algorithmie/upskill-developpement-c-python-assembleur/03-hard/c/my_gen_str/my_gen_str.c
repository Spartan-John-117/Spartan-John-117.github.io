#include <stdarg.h> 
#include <stdlib.h> 
#include <string.h> 
#include <ctype.h>  

char* my_gen_str(char * const __format, ...) {
                                                                                // Vérifie si le format est NULL
    if (!__format) {
        return NULL;
    }

                                                                                // Initialisation de la liste d'arguments variadiques
    va_list args;
    va_start(args, __format);

                                                                                // Tableau pour stocker les arguments correspondant aux placeholders
    char *placeholders[1000] = {NULL};
    int index = 0;

                                                                                // Récupère les arguments dans le tableau jusqu'à rencontrer NULL
    char *arg;
    while ((arg = va_arg(args, char *)) != NULL) {
        if (index < 1000) {
            placeholders[index++] = arg;
        }
    }
    va_end(args);

                                                                                // Allocation initiale pour la chaîne de sortie
    size_t output_size = strlen(__format) + 1;
    char *output = malloc(output_size);
    if (!output) {
        return NULL;                                                            // Erreur d'allocation
    }
    output[0] = '\0';                                                           // Initialise la chaîne de sortie

                                                                                // Parcours de la chaîne de format
    for (size_t i = 0; __format[i] != '\0'; i++) {
        if (__format[i] == '{') {
            if (__format[i + 1] == '{') {                                       // Cas des accolades doubles "{{"
                output_size += 1;
                output = realloc(output, output_size);
                if (!output) return NULL;
                strcat(output, "{");                                            // Ajoute une accolade littérale
                i++;                                                            // Sauter la deuxième accolade
            } else {
                                                                                // Rechercher la fermeture de l'accolade "}"
                size_t j = i + 1;
                while (__format[j] != '\0' && __format[j] != '}') {
                    j++;
                }

                if (__format[j] == '}') {                                       // Placeholder trouvé
                    char placeholder[10] = {0};
                    strncpy(placeholder, &__format[i + 1], j - i - 1);

                                                                                // Supprimer les espaces autour du placeholder
                    size_t start = 0, end = strlen(placeholder);
                    while (start < end && isspace(placeholder[start])) start++;
                    while (end > start && isspace(placeholder[end - 1])) end--;
                    placeholder[end - start] = '\0';

                                                                                // Convertir le placeholder en index entier
                    int ph_index = -1;
                    if (isdigit(placeholder[0])) {
                        ph_index = atoi(placeholder);
                    }

                                                                                // Remplacer le placeholder par l'argument correspondant
                    if (ph_index >= 0 && ph_index < index && placeholders[ph_index]) {
                        output_size += strlen(placeholders[ph_index]);
                        output = realloc(output, output_size);
                        if (!output) return NULL;
                        strcat(output, placeholders[ph_index]);
                    } else {
                                                                                // Placeholder invalide, copier tel quel
                        output_size += (j - i + 1);
                        output = realloc(output, output_size);
                        if (!output) return NULL;
                        strncat(output, &__format[i], j - i + 1);
                    }

                    i = j;                                                      // Avancer après "}"
                } else {
                                                                                // Placeholder mal formé, copier "{" tel quel
                    output_size += 1;
                    output = realloc(output, output_size);
                    if (!output) return NULL;
                    strncat(output, &__format[i], 1);
                }
            }
        } else if (__format[i] == '}') {
            if (__format[i + 1] == '}') {                                       // Cas des accolades doubles "}}"
                output_size += 1;
                output = realloc(output, output_size);
                if (!output) return NULL;
                strcat(output, "}");                                            // Ajoute une accolade littérale
                i++;                                                            // Sauter la deuxième accolade
            } else {
                                                                                // Copie une accolade fermante isolée
                output_size += 1;
                output = realloc(output, output_size);
                if (!output) return NULL;
                strncat(output, &__format[i], 1);
            }
        } else {
                                                                                // Ajouter un caractère ordinaire à la chaîne de sortie
            output_size += 1;
            output = realloc(output, output_size);
            if (!output) return NULL;
            strncat(output, &__format[i], 1);
        }
    }

    return output;                                                              // Retourne la chaîne formatée
}