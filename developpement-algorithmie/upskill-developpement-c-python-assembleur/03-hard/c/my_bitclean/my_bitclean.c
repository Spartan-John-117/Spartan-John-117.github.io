#include "my_bitclean.h"

uint32_t my_bitclean(uint32_t __bitmap, int __pos) 
{
    if (__pos == 0) 
    {
        return __bitmap & ~1U;                                  // Effectue un ET bit à bit (les bits des deux valeurs
                                                                // doivent être à 1, pour que le résultat soit 1) 
                                                                // entre la valeur binaire de __bitmap et de l'inverse (~) 
                                                                // de la valeur binaire de 1 (U = non signé)
                                                                // 1U =  000...001
                                                                // ~1U = 111...110
                                                                // Comme le bit de poids faible (à droite) est à 0, le
                                                                // nombre est forcément pair
    } 
        else if (__pos > 0 && __pos < 32) 
        {
            return __bitmap & ~(1U << __pos);                   // Ecrit un 1 à l'emplacement donné par pos et l'inverse
                                                                // donc seul le bit indiqué par pos est à 0
                                                                // Effectue un ET binaire (&) entre __ bitmap et le résultat
                                                                // obtenu entre parenthèses
                                                                // (1U << 2) =  ...0100
                                                                // ~(1U << 2) = ...1011
        } 
        else 
        {
            int negative_pos = 31 + __pos;                      // Convertit une position négative en positive
            if (negative_pos >= 0 && negative_pos < 32)         // La position doit être comprise entre 0 et 31 (entier 32 bits non signés)
            {
                return __bitmap & ~(1U << negative_pos);        // Effectue un & entre __bitmap et l'inverse de 1 (à la position
                                                                // negative_pos)
            }   
        }
        return __bitmap;                                        // La fonction doit retourner un résultat par défaut sinon compile_error
}
