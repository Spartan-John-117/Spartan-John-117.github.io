import sys
import math
from collections import Counter

# Définir les points pour chaque lettre
points = {
    'e': 1, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1, 't': 1, 'l': 1, 's': 1, 'u': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 8, 'x': 8,
    'q': 10, 'z': 10
}

# Lire la liste des mots
word_list = []
n = int(input())
for _ in range(n):
    word_list.append(input())

# Lire les lettres disponibles
letters = input()

# Fonction pour calculer le score d'un mot
def score_word(word):
    return sum(points[char] for char in word)

# Fonction pour vérifier si un mot peut être formé avec les lettres disponibles
def can_form_word(word, available_letters):
    word_count = Counter(word)
    available_count = Counter(available_letters)
    for char in word_count:
        if word_count[char] > available_count.get(char, 0):
            return False
    return True

# Initialiser le meilleur mot et le score maximal
best_word = ""
max_score = 0

# Parcourir tous les mots et trouver celui avec le score maximal
for word in word_list:
    if can_form_word(word, letters):
        current_score = score_word(word)
        if current_score > max_score:
            max_score = current_score
            best_word = word

# Afficher le meilleur mot
print(best_word)
