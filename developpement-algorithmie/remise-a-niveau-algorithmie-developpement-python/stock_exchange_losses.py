import sys
import math

# Initialisation de la liste des valeurs et de la perte maximale
liste_v = []
max_perte = float('inf')  # Initialiser à l'infini pour trouver la perte maximale négative
n = int(input())
for i in input().split():
    liste_v.append(int(i))

#print(liste_v)

# Variable pour garder la valeur maximale rencontrée
valeur_max = liste_v[0]

# Calcul de la perte maximale
for i in range(1, len(liste_v)):
    # Si une nouvelle valeur maximale est trouvée, on la met à jour
    if liste_v[i] > valeur_max:
        valeur_max = liste_v[i]
    # Sinon, on calcule la perte par rapport à la valeur maximale
    else:
        perte = liste_v[i] - valeur_max
        if perte < max_perte:
            max_perte = perte

if max_perte == float('inf'):
    max_perte = 0

# Affichage du résultat
print(max_perte)
