# my_parser — mini-parser pour "minilang"

Ce dossier contient un petit parseur écrit en C pour un langage d'exemple (fichier de grammaire : `minilang.peg`). Le projet fournit aussi des tests unitaires basiques basés sur la bibliothèque Criterion.

Objectif
--------
Le parseur permet de scanner et d'extraire des constructions syntaxiques d'un langage minimal (nombres, identifiants, flottants, opérations arithmétiques, captures d'AST...). Il sert de démonstrateur pédagogique pour la construction d'un parseur manuel (sans générateur automatique).

Contenu important
-----------------
- `my_parser.c` — implémentation des primitives de lecture : caractères, plages, identifiants, entiers, float, gestion des positions, captures d'AST et utilitaires.
- `include/my_parser.h` — prototype des fonctions publiques et structures (parser, capture_list, position).
- `minilang.peg` — description de la grammaire (PEG) du langage ciblé, utile comme spécification.
- `test_my_parser.c` — tests unitaires qui valident les primitives fondamentales du parseur (utilise Criterion).
- `Makefile` — tâches make : compilation, test, nettoyage.
- `test` et fichiers objets (`*.o`) — sorties de compilation (peuvent être supprimées avec `make clean`).

Prérequis
---------
- GCC (ou un compilateur C compatible C99)
- make
- Criterion (lib et headers) — la Makefile cherche la librairie dans `./lib` et les headers dans `include/criterion`.

Compilation et tests
--------------------
1. Compiler les objets :

```bash
make
```

2. Lancer la suite de tests (si Criterion est disponible) :

```bash
make test
```

La cible `test` lie le binaire de test avec Criterion et exécute le binaire (le Makefile utilise `timeout 1m` pour limiter la durée).

Nettoyage
---------
- Pour supprimer les objets :

```bash
make clean
```

- Pour supprimer aussi l'exécutable de tests :

```bash
make distclean
```

Utilisation et extension
------------------------
- `minilang.peg` peut être utilisé comme spécification pour compléter/adapter le parseur. Les fonctions présentes dans `my_parser.c` sont des primitives utiles pour implémenter la lecture des règles décrites dans la grammaire.
- La gestion d'AST est partiellement implémentée via `capture_list` et des fonctions `begin_capture` / `end_capture` / `get_node` / `get_value`.
- Pour ajouter de nouvelles règles, éditez `my_parser.c` et ajoutez des fonctions qui consomment la chaîne d'entrée en utilisant les primitives fournies (`readchar`, `readtext`, `readint`, `readfloat`, etc.).

Tests unitaires
---------------
Le fichier `test_my_parser.c` contient plusieurs cas de test (Criterion) qui servent d'exemples d'utilisation des primitives :
- vérification de `readeof`, `readchar`, `readtext`, `readrange`, `readint`, `readid`, `readfloat` (décimal, fraction, exposant).