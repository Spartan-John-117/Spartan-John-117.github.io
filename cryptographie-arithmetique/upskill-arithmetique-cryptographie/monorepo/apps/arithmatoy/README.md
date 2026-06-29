# Projet - Arithmatoy

## Sujet

L'objectif de ce projet est d'implémenter en C les algorithmes d'addition, soustraction et multiplication vu à l'école primaire.

L'implémentation doit fonctionner dans n'importe quelle base de 2 à 36, utilisant les chiffres parmis: `0123456789abcdefghijklmnopqrstuvwxyz`. Par exemple, le nombre 35 peut s'écrire:

- `35` en base 10
- `100011` en base 2
- `23` en base 16 (hexadécimal)
- `z` en base 36
- `10` en base 35

Votre role est d'implémenter les fonction `arithmatoy_add`, `arithmatoy_sub` et `arithmatoy_mul` définies dans [arithmatoy.c](src/arithmatoy.c).

A l'issue de votre implémentation, l'ensemble des tests du projet doivent passer.

Plusieurs fonctions utilitaires vous sont données pour faciliter l'implémentation.

**Attention**: Vous devez implémenter les algorithmes directement sur les chaines de caractère d'entrée des fonctions, pas convertir ces chaines en nombre pour faire le calcul. En particulier vos fonctions doivent gérer des nombres arbitrairement grands.

En plus de cela, si la variable `VERBOSE` vaut `1`, il faudra afficher des logs sur stderr indiquant les étapes intermédiaires des calculs (opérations sur chiffres et retenues). Les logs à afficher doivent avoir le même format que ceux que vous trouverez dans les fichiers sous [`tests/outputs/`](tests/outputs). Ces fichiers ont été généré avec mon implémentation et vous pouvez utiliser les tests de non regression python du projet pour valider que votre programme produit les même logs.

## Mise en place de l'environnement de build

Vous aurez besoin à minima de CMake et un compilateur C. La configuration conseillée est gcc sous Linux/Mac, Visual Studio sous Windows, mais vous êtes libre d'adapter à votre cas d'utilisation. Le projet est configuré pour l'editeur Visual Studio Code pour tout ce qui est configuration de debug et formattage automatique.

- Si vous etes sous linux, assurez vous d'installer l'outil pkg-config: `sudo apt-get install pkg-config` par example sous Ubuntu

Depuis la racine du monorepo, lancez la commande:

```bash
rye run arithmatoy setup
```

Cette commande ne doit être lancée qu'une fois. Elle installe l'utilitaire [`vcpkg`](https://vcpkg.io/en/index.html) et la dépendance [`cmocka`](https://cmocka.org/). CMocka est une bibliothèque de test unitaire en C.

## Développement

Pour compiler le projet:

```bash
rye run arithmatoy build
```

Pour lancer les tests en C:

```bash
rye run arithmatoy ctest
# Egalement possible de lancer les tests d'une seule fonction:
rye run arithmatoy ctest --test=test_add
rye run arithmatoy ctest --test=test_sub
rye run arithmatoy ctest --test=test_mul
```

Les tests devraient échouer, vous devez implémenter les fonctions pour les faire passer.

A chaque modification des fichiers source C il faut recompiler le projet, mais la commande pour lancer les tests le fait automatiquement par défaut. Pour lancer les tests sans re-compiler:

```bash
rye run arithmatoy ctest --no-rebuild
```

Toutes les commandes compilent en mode debug par défaut (ce qui vous permet de débugguer avec un outil comme gdb sous linux, ou le débugger Visual Studio sous windows).

Pour compiler et lancer les tests en mode release:

```bash
rye run arithmatoy build --mode release
rye run arithmatoy ctest --mode release
```

## Lancer l'executable compilé

Le dossier de build produit par CMake est `.local/build` sous lequel vous trouvez les dossiers `debug` et `release` sous windows, ou l'executable directement sous linux.

La commande de compilation installe également l'executable sous `local/dist/bin`. Pour lancer l'executable, depuis la racine du monorepo:

```bash
.local/cmake/dist/bin/arithmatoy-cli
```

Le lancement affiche une ligne d'aide décrivant les arguments à passer. Quelques examples:

```bash
.local/cmake/dist/bin/arithmatoy-cli add 2 0 1 # Addition 0 + 1 en base 2, doit afficher 0 + 1 = 1
.local/cmake/dist/bin/arithmatoy-cli add 10 256 128 # Addition 256 + 128 en base 10, doit afficher 256 + 128 = 384
.local/cmake/dist/bin/arithmatoy-cli add 16 ff a2 # Addition ff + a2 en base 16, doit afficher ff + a2 = 1a1
.local/cmake/dist/bin/arithmatoy-cli mul 16 ff a2 # Multiplication ff * a2, doit afficher ff * a2 = a15e
.local/cmake/dist/bin/arithmatoy-cli sub 16 ff a2 # Soustraction ff - a2, doit afficher ff - a2 = 5d
```

## Mode verbose

Le mode verbose doit être implémenté de sorte à afficher un certain nombre de logs vous permettant de débugguer, et me permettant de vous corriger de manière plus précise afin de vérifier que vous implémentez bien les algorithmes demandés.

Prenons un example:

```bash
.local/cmake/dist/bin/arithmatoy-cli add 10 1924 128 --verbose
```

L'executable de correction affiche le log suivant:

```bash
add: entering function
add: digit 4 digit 8 carry 0
add: result: digit 2 carry 1
add: digit 2 digit 2 carry 1
add: result: digit 5 carry 0
add: digit 9 digit 1 carry 0
add: result: digit 0 carry 1
add: digit 1 digit 0 carry 1
add: result: digit 2 carry 0
1924 + 128 = 2052
```

Cette suite de log décrit l'ensemble des opérations que l'on effectue en posant une addition, avec l'état de la retenue à chaque ligne. La retenue commence à 0, puis évolue. On a ainsi la traduction litérale:

- Je lis 4 + 8, ma retenue est 0 (`add: digit 4 digit 8 carry 0`)
- Le résultat est 4 + 8 + 0 = 12, je pose 2 je retiens 1 (`add: result: digit 2 carry 1`)
- Je lis 2 + 2, ma retenue est 1 (`add: digit 2 digit 2 carry 1`)
- Le résultat est 2 + 2 + 1 = 5, je pose 5 je retiens 0 (`add: result: digit 5 carry 0`)
- Je lis 9 + 1, ma retenue est 0 (`add: digit 9 digit 1 carry 0`)
- Le résultat est 9 + 1 + 0 = 10, je pose 0 je retiens 1 (`add: result: digit 0 carry 1`)
- Je lis 1 + 0, ma retenue est 1 (`add: digit 1 digit 0 carry 1`)
- Le résultat est 1 + 0 + 1 = 2, je pose 2 je retiens 0 (`add: result: digit 2 carry 0`)
- Le résultat final est `1924 + 128 = 2052`, obtenue par concaténation de toutes les poses

Voici les logs pour la soustraction:

```bash
.local/cmake/dist/bin/arithmatoy-cli sub 10 1924 128 --verbose
sub: entering function
sub: digit 4 digit 8 carry 0
sub: result: digit 6 carry 1 # on a 4 < 8, on pose 10 + 4 - 8 = 6, on retient 1
sub: digit 2 digit 2 carry 1 # La retenue s'additionne au deuxième chiffre => on prendra 2 + 1 = 3 en dessous
sub: result: digit 9 carry 1 # on a 2 < 3, on pose 10 + 2 - 3 = 9, on retient 1
sub: digit 9 digit 1 carry 1 # La retenue s'additionne au deuxième chiffre => on prendre 1 + 1 = 2 en dessous
sub: result: digit 7 carry 0 # on a 9 > 2, on pose 9 - 2 = 7, pas de retenue
sub: digit 1 digit 0 carry 0
sub: result: digit 1 carry 0 # on a 1 > 0, on pose 1 - 0 = 1, pas de retenue
1924 - 128 = 1796 # On concatène tout ce qui a été posé
```

L'algorithme de la soustraction est plus complexe mais vous pourrez le retrouver en ligne.

Enfin la multiplication:

```bash
.local/cmake/dist/bin/arithmatoy-cli mul 10 1924 128 --verbose
mul: entering function
mul: digit 8 number 1924
mul: digit 8 digit 4 carry 0
mul: result: digit 2 carry 3
mul: digit 8 digit 2 carry 3
mul: result: digit 9 carry 1
mul: digit 8 digit 9 carry 1
mul: result: digit 3 carry 7
mul: digit 8 digit 1 carry 7
mul: result: digit 5 carry 1
mul: final carry 1
mul: add 0 + 15392
add: entering function
add: digit 2 digit 0 carry 0
add: result: digit 2 carry 0
add: digit 9 digit 0 carry 0
add: result: digit 9 carry 0
add: digit 3 digit 0 carry 0
add: result: digit 3 carry 0
add: digit 5 digit 0 carry 0
add: result: digit 5 carry 0
add: digit 1 digit 0 carry 0
add: result: digit 1 carry 0
mul: result: 15392
mul: digit 2 number 1924
mul: digit 2 digit 4 carry 0
mul: result: digit 8 carry 0
mul: digit 2 digit 2 carry 0
mul: result: digit 4 carry 0
mul: digit 2 digit 9 carry 0
mul: result: digit 8 carry 1
mul: digit 2 digit 1 carry 1
mul: result: digit 3 carry 0
mul: add 15392 + 38480
add: entering function
add: digit 2 digit 0 carry 0
add: result: digit 2 carry 0
add: digit 9 digit 8 carry 0
add: result: digit 7 carry 1
add: digit 3 digit 4 carry 1
add: result: digit 8 carry 0
add: digit 5 digit 8 carry 0
add: result: digit 3 carry 1
add: digit 1 digit 3 carry 1
add: result: digit 5 carry 0
mul: result: 53872
mul: digit 1 number 1924
mul: digit 1 digit 4 carry 0
mul: result: digit 4 carry 0
mul: digit 1 digit 2 carry 0
mul: result: digit 2 carry 0
mul: digit 1 digit 9 carry 0
mul: result: digit 9 carry 0
mul: digit 1 digit 1 carry 0
mul: result: digit 1 carry 0
mul: add 53872 + 192400
add: entering function
add: digit 0 digit 2 carry 0
add: result: digit 2 carry 0
add: digit 0 digit 7 carry 0
add: result: digit 7 carry 0
add: digit 4 digit 8 carry 0
add: result: digit 2 carry 1
add: digit 2 digit 3 carry 1
add: result: digit 6 carry 0
add: digit 9 digit 5 carry 0
add: result: digit 4 carry 1
add: digit 1 digit 0 carry 1
add: result: digit 2 carry 0
mul: result: 246272
1924 * 128 = 246272
```

Ici le log est nettement plus long car l'algorithme de la multiplication consiste en une itération de l'addition. Cela peut se voir dans les logs: toutes les lignes commençant par `add:` montre une addition intermédiaire et suggère que mon implémentation de la multiplication fait appel à la fonction codée pour l'addition.

## Lancer les tests de non regression python

Les tests pythons ont pour objectif de tester votre executable sur un grand nombre d'examples, avec différentes bases. Pour cela, ces tests comparent la sortie de votre executable avec une sortie produite par mon implémentation. L'ensemble des sorties attendues sont stockés dans les fichiers texte sous `tests/outputs/[test_add|test_mul|test_sub]`.

Il est important d'avoir compilé l'executable avant de lancer les tests python, sinon vous aurez une erreur. Il est deplus conseillé de compiler en mode release avant d'avoir une execution plus rapide:

```bash
rye run arithmatoy build --mode release
```

Vous pouvez ensuite lancer les tests via les commandes suivantes:

```bash
rye run pytest -k test_arithmatoy_add_noverbose
rye run pytest -k test_arithmatoy_add_verbose
rye run pytest -k test_arithmatoy_sub_noverbose
rye run pytest -k test_arithmatoy_sub_verbose
rye run pytest -k test_arithmatoy_mul_noverbose
rye run pytest -k test_arithmatoy_mul_verbose
```

Chaque ligne va lancer un grand nombre d'opération avec la fonction `add`, `sub` ou `mul`, en mode verbose ou non selon le test lancé.

Note: Si votre éditeur est VSCode, il devrait détecter les tests python et vous permettre de les lancer depuis un panel de l'editeur.

## Conseils pour le développement

Ce projet n'est pas simple et il est important de développement itérativement, par essais-erreurs, et ne pas essayer de tout coder d'un seul coup en espérant passer tous les tests directement. Faites régulièrement des commits afin de sauvegarder votre avancée lorsqu'un nouvel élement fonctionne.

Commencez par implémenter la fonction d'addition `arithmatoy_add` sans s'occuper du mode verbose, et essayer de faire passer ses tests en C:

```bash
rye run arithmatoy ctest --test=test_add
```

Ne pas hésiter a débugguer avec des `printf` (ou mieux des breakpoint en debug) jusqu'a passer le test. Lire également le code des tests dans `src/tests/test_add.c` pour comprendre quels cas pose problèmes. Ajouter des tests si nécessaire. Lancer manuellement votre executable avec:

```bash
.local/cmake/dist/bin/arithmatoy-cli add [base] [left] [right]
```

afin d'itérer sur certains cas problématiques.

Une fois que le test C passe, lancer le test python en no verbose:

```bash
rye run pytest -k test_arithmatoy_add_noverbose
```

Si ce test ne passe pas alors que le test C passe c'est que votre code ne couvre pas certains cas. Identifiez ces cas grace aux fichiers texte sous `tests/outputs` et continuez de débugguer votre code jusqu'à ce que ça passe.

Une fois que tout fonctionne, mettez les `fprintf` nécessaire dans des blocs `if (VERBOSE) {}` afin d'implémenter le mode verbose avec les logs tels que décrit plus haut. Les fichiers texte `tests/outputs` contiennent de nombreux exemples de logs. Corrigez votre implémentation jusqu'a ce que le test suivant passe:

```bash
rye run pytest -k test_arithmatoy_add_verbose
```

Pensez a lancer manuellement votre executable avec l'option `--verbose` pour débugguer plus facilement des cas précis:

```bash
.local/cmake/dist/bin/arithmatoy-cli add [base] [left] [right] --verbose
```

Une fois que tout fonctionne pour l'addition, passez à la soustraction, puis finissez par la multiplication. Bon courage !

## Notation

La notation sera faite automatiquement via un script selon le barème suivant:

- Test C qui passe: +3 points
- Test python qui passe, sans verbose: +2 points
- Test python qui passe, avec verbose: +2 points

Chaque fonction `add`, `sub` et `mul` est donc notée sur 7 points, pour un total de 21 points, qui sera ramené à 20 en tronquant simplement.
