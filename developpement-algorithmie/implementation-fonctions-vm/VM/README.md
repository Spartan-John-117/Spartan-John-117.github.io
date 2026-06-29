# Mini-Projet : Simulateur de Machine Virtuelle Vm[SUPPRIME_2600] v2.0

> [!WARNING]
> Tous les fichiers ne sont pas inclus, seulement ceux que j'ai complété. Donc la vm n'est pas fonctionnelle en l'état.

Ce projet consiste à finaliser un simulateur pour une machine virtuelle simple, la **Vm[SUPPRIME_2600] v2.0**. Le travail est divisé en deux étapes principales, qui impliquent de modifier trois fichiers Python fournis.

## Étape 1 : Intégrer l'encodage et le décodage

-   **Fichiers à modifier :** `minivm_decode.py` et `minivm_encode.py`.
-   **Tâche :** Vous devez compléter les fonctions pour encoder et décoder les instructions, de manière similaire à ce qui a été fait dans les exercices préparatoires 4 et 5 de Codingame.
-   **Attention :** Le format de la valeur de préfixe est différent (un `'unsigned char'` plutôt qu'un simple caractère).

## Étape 2 : Compléter les instructions de la machine virtuelle

-   **Fichier à modifier :** `minivm_insn.py`.
-   **Tâche :** C'est la partie la plus conséquente. Vous devez implémenter la logique pour l'ensemble des instructions de la Vm[SUPPRIME_2600]. Cela inclut :
    -   **Opérations arithmétiques et logiques :** `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `AND`, `OR`, `XOR`.
    -   **Instructions de saut :** `JMP`, `JE`, `JNE`, `CALL`, `RET`.
    -   **Manipulation des données et des registres :** `MOV`, `PUSH`, `POP`.
    -   **Chargement de constantes :** `LOADINT`, `LOADSTR`.
    -   **Gestion des "cadres de pile" pour les variables locales :** `ENTER`, `LEAVE`, `FETCH`, `STORE`.
    -   **Opérations sur les chaînes de caractères :** `GETAT`, `SETAT`, `LENSTR`.
    -   **Conversions de type :** `CASTINT`, `CASTSTR`, `ORD`, `CHR`.

## Objectif final (Étape 3 : It Works!)

Le but est de rendre la machine virtuelle fonctionnelle. Si le fichier `minivm_insn.py` est complété correctement, vous devriez être capable d'exécuter le programme `test.vm[SUPPRIME_2600]`.
