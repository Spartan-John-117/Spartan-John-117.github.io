import sys
import math

# Lire les entrées
l = int(input())  # Largeur d'une lettre en art ASCII
h = int(input())  # Hauteur d'une lettre en art ASCII
t = input().upper()  # Ligne de texte à convertir en majuscules

# Lire l'art ASCII des lettres A-Z et du caractère '?'
ascii_art = []
for i in range(h):
    ascii_art.append(input())

# Initialiser la liste pour stocker le résultat final
output = [""] * h

# Parcourir chaque caractère de la chaîne de texte T
for char in t:
    if 'A' <= char <= 'Z':  # Si le caractère est une lettre majuscule
        index = ord(char) - ord('A')
    else:  # Si le caractère est autre (non A-Z), utiliser '?'
        index = 26  # '?' est à la position 26

    # Construire chaque ligne du texte en art ASCII
    for i in range(h):
        output[i] += ascii_art[i][index * l : (index + 1) * l]

# Afficher le résultat final
for line in output:
    print(line)
