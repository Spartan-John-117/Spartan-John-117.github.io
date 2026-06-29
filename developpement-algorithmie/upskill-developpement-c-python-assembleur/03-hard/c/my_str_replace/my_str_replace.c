#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "my_str_replace.h"

char *strdup(const char *s) {
    size_t len = strlen(s) + 1;
    char *copy = malloc(len);
    if (copy) {
        memcpy(copy, s, len);
    }
    return copy;
}

char *my_str_replace(const char *old_pat, const char *str, const char *new_pat) {
    // Cas où str est NULL
    if (str == NULL) {
        return NULL;
    }

    // Cas où old_pat est NULL ou vide (insérer new_pat entre chaque caractère de str)
    if (old_pat == NULL || old_pat[0] == '\0') {
        if (new_pat == NULL) {  // Si new_pat est NULL, on retourne une copie de str
            return strdup(str);
        }

        size_t len = strlen(str);
        size_t new_pat_len = strlen(new_pat);
        size_t new_len = len + (new_pat_len * (len - 1)) + new_pat_len; // Nouvelle longueur

        // Allouer de la mémoire pour la chaîne résultat
        char *result = malloc(new_len + 1);
        if (!result) {
            return NULL;  // Allocation échouée
        }

        size_t i, j = 0;

        // Ajouter new_pat avant le premier caractère
        strcpy(result + j, new_pat);
        j += new_pat_len;

        // Ajouter new_pat entre chaque caractère de str
        for (i = 0; i < len; ++i) {
            result[j++] = str[i];
            if (i < len - 1) {
                strcpy(result + j, new_pat);  // Ajouter new_pat après chaque caractère sauf le dernier
                j += new_pat_len;
            }
        }
        // Ajouter new_pat après le dernier caractère
        strcpy(result + j, new_pat);
        j += new_pat_len;

        result[j] = '\0';  // Ajouter la fin de la chaîne
        return result;
    }

    // Cas classique où old_pat n'est pas NULL
    size_t str_len = strlen(str);
    size_t old_pat_len = strlen(old_pat);
    size_t new_pat_len = (new_pat == NULL) ? 0 : strlen(new_pat);
    size_t count = 0;  // Compter combien de fois old_pat apparaît dans str

    // Calculer le nombre d'occurrences de old_pat dans str
    const char *tmp = str;
    while ((tmp = strstr(tmp, old_pat)) != NULL) {
        ++count;
        tmp += old_pat_len;
    }

    // Calculer la taille de la chaîne résultante
    size_t result_len = str_len - (count * old_pat_len) + (count * new_pat_len);
    char *result = malloc(result_len + 1);  // +1 pour le caractère de fin de chaîne
    if (!result) {
        return NULL;  // Allocation échouée
    }

    // Remplir le résultat avec les remplacements
    size_t i = 0, j = 0;
    while (str[i] != '\0') {
        if (strstr(&str[i], old_pat) == &str[i]) {
            strcpy(&result[j], new_pat);  // Si on trouve old_pat, on le remplace par new_pat
            j += new_pat_len;
            i += old_pat_len;
        } else {
            result[j++] = str[i++];
        }
    }
    result[j] = '\0';  // Ajouter la fin de chaîne

    return result;
}