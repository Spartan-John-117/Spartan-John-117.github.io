# my_calc — mini-calculatrice / parseur (dossier my_calc)

Ce dossier contient une implémentation en C d'un petit langage de calcul (grammaire disponible dans `minilang.peg`) et le parseur associé. Le projet sert d'exemple pédagogique pour construire un parseur manuel, manipuler des captures (AST simples) et valider les primitives via des tests unitaires.

Résumé
------
- Langage : expressions arithmétiques avec entiers, parenthèses, opérateurs + - * / % ^ (puissance), assignations de variables sous la forme `name = expression;` et lignes terminées par `;`.
- Fichiers principaux : implémentation des règles du langage (`my_calc.c`), primitives du parseur (`my_parser.c`), en-têtes (`include/`), et tests (`test_my_calc.c`, `test_my_parser.c`).

Structure
---------
- `minilang.peg` : définition PEG du langage (spécification).
- `my_calc.c` : implémentation des règles (exponent, mult, add, primary, line, my_calc, etc.) — compose les primitives fournies par `my_parser` pour construire l'analyseur.
- `my_parser.c` : primitives du parseur (lecture de caractères, ranges, textes, floats, captures d'AST, gestion de position, espaces/commentaires).
- `include/` : headers publics (`my_calc.h`, `my_parser.h`).
- `test_my_calc.c`, `test_my_parser.c` : tests unitaires (Criterion).
- `Makefile` : règles `make`, `make test`, `make clean`, `make distclean`.
- `tests/` : dossier réservé aux entrées/sorties de tests (si présent).

Prérequis
---------
- GCC ou compilateur C compatible C99
- make
- Criterion (lib + headers) pour exécuter la suite de tests (ou placer les headers/librairies de Criterion dans `include/criterion` et `./lib` si souhaité)

Compilation
-----------
Depuis le dossier `my_calc` :

```bash
make
```

La cible `make` construit les objets (et éventuellement l'exécutable de test selon le Makefile). Pour exécuter les tests unitaires :

```bash
make test
```

(Remarque : le Makefile fourni exécute `timeout 1m ./test` pour limiter la durée d'exécution des tests.)

Nettoyage
---------
- Supprimer les fichiers objets :

```bash
make clean
```

- Supprimer aussi l'exécutable de test :

```bash
make distclean
```

Utilisation (exemple minimal)
-----------------------------
Le dépôt n'inclut pas forcément un binaire interactif prêt à l'emploi, mais la logique de parsing est accessible via l'API `new_parser` / `my_calc`. Exemple d'usage (idée) :

```c
struct parser *p = new_parser("a = 2 + 3; b = a^2;");
struct scope s = {0};
if (my_calc(p, &s)) {
    // s.current_val contient la dernière valeur évaluée
}
clean_parser(p);
```

Si vous voulez un exécutable en ligne de commande, ajoutez un `main.c` qui lit un fichier ou stdin, appelle `new_parser` puis `my_calc` et affiche le résultat.

Précisions sur le langage
------------------------
- Les nombres traités sont des entiers (les fonctions utilisent `long` pour la valeur actuelle). Un support flottant partiel est présent dans les primitives du parseur (`readfloat`) mais la grammaire et la sémantique du module `my_calc` opèrent sur des entiers.
- Les commentaires supportés dans `read_space` : `//` pour les commentaires sur une ligne et `/* ... */` pour les commentaires multi-lignes.
- Les assignations sont stockées dans une liste chaînée (`def_list`) accessible via les fonctions `prepend_in_scope`, `get_in_scope`, `clean_in_scope`.

Tests
-----
Les tests fournis montrent l'utilisation et valident :
- les primitives (lecture d'entiers, identifiants, floats),
- la reconnaissance des espaces et commentaires,
- l'évaluation des expressions (puissance, multiplication/division/modulo, addition/soustraction),
- les assignations et la persistance des variables dans le scope.