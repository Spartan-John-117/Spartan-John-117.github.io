# Maths

## Mise en place

Le repo est multi plateform Linux / Windows, possiblement OSX.

- Créez un compte Gitlab
- Forkez le repository sur votre compte Gitlab
- Installez les outils de développement suivant:
  - [Rye](https://rye.astral.sh/guide/installation/): pour environnement de développement python isolé
  - [CMake](https://cmake.org/): pour compilation projet Arithmatoy en C
  - [Git](https://git-scm.com/downloads)
  - [VSCode](https://code.visualstudio.com/) avec les extensions conseillées:
    - [Git graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)
- Clonez votre fork localement

Ouvrez le dossier du repo local dans VSCode, ouvrez un terminal, et lancez la commande suivante:

```bash
rye sync
```

Rye est un outil de gestion de projet et dépendances python proposant une experience de développement moderne.
La commande `rye sync` créé un environnement virtuel dans `.venv` à la racine, avec son propre python isolé du python système, et installe l'ensemble des dépendances du projet.

Les tests vont échouer, mais vous devez ensuite pouvoir lancer `pytest` avec la commande `rye run pytest`.
Faire passer les tests est l'objectif des TPs et projets.

Vous pouvez également lancer ces tests depuis le panel de tests de VSCode. C'est particulièrement conseillé pour pouvoir débugguer avec breakpoints.

## TPs et projets

Vous serez guidés pendant les cours vers chacun des sous projets situés dans `apps/`. Chacun possède son README expliquant ses détails. La plupart du code à écrire est en python, sauf Arithmatoy en C.

- [tp-nombres](apps/tp-nombres/README.md): exercices qui seront donnés pendant les cours / TPs, thématique nombres et algorithmique numérique
- [arithmatoy](apps/arithmatoy/README.md): premier projet, en C, implémentation de l'addition, soustraction et multiplication
- [turingtoy](apps/turingtoy/README.md): deuxième projet, implémentation de la simulation de machines de Turing
- [cryptoy](apps/cryptoy/README.md): exercices qui seront donnés pendant les cours / TPs, thématique cryptographie

## Optionnel: lancer les slides localement

Si vous désirez les lancer localement:

- Installez [nodejs](https://nodejs.org/fr)
- Installez [pnpm](https://pnpm.io/)

Puis à la racine lancez `pnpm install`

Cette commande installe les dépendances nodejs du projet. Ensuite dans un sous dossier de `slides/`:

```bash
cd slides/001-slides-nombres # Remplacer par n'importe quel autre sous dossier
pnpm dev
```

Cette commande lance un serveur web de développement donnant accès aux slides sur une URL locale. Les slides sont implémentées en markdown dans un fichier `slides.md` pour chaque sous projets.
