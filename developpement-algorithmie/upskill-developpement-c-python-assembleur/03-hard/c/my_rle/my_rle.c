#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *rle_encode(const char *s) {                                       // Fonction pour encoder la chaîne en RLE
    int len = strlen(s);
    char *encoded = (char *)malloc(2 * len + 1);                        // Allouer de la mémoire pour le résultat
    if (!encoded) {
        return NULL;                                                    // En cas d'échec de l'allocation
    }
    int i = 0, j = 0;
    while (i < len) {
        char current_char = s[i];
        int count = 1;

        while (i + 1 < len && s[i + 1] == current_char && count < 9) {  // Compte le nombre de caractères successifs identiques
            i++;
            count++;
        }
        encoded[j++] = count + '0';                                     // Convertir le nombre en caractère
        encoded[j++] = current_char;

        i++;                                                            // Passer au caractère suivant
    }

    encoded[j] = '\0';                                                  // Terminer la chaîne par un caractère nul
    return encoded;
}
char *rle_decode(const char *s) {                                       // Fonction pour décoder une chaîne en RLE
    int len = strlen(s);
    int decoded_len = 0;

    for (int i = 0; i < len; i += 2) {                                  // Calculer la longueur de la chaîne décodée
        decoded_len += s[i] - '0';                                      // Le nombre d'occurrences se trouve à la position i
    }
    char *decoded = (char *)malloc(decoded_len + 1);                    // Allouer de la mémoire pour la chaîne décodée
    if (!decoded) {
        return NULL;                                                    // En cas d'échec de l'allocation
    }

    int k = 0;
    for (int i = 0; i < len; i += 2) {
        int count = s[i] - '0';                                         // Le nombre d'occurrences se trouve à la position i
        char current_char = s[i + 1];

        for (int j = 0; j < count; j++) {                               // Ajouter les caractères décodés
            decoded[k++] = current_char;
        }
    }

    decoded[k] = '\0';                                                  // Terminer la chaîne par un caractère nul
    return decoded;
}
