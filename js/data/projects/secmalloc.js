window.projectData = window.projectData || {};
window.projectData["secmalloc"] = {
    title: "Implémentation secmalloc",
    domain: "Cybersécurité",
    technologies: ["C", "Makefile", "Valgrind", "Criterion"],
    content: `
## my_secmalloc

Comme l'illustre l'antique papier de Phrack.org *Malloc des maleficarum*, les
fonctions de \`malloc\` sont sujettes à de nombreux détournements. Même si, depuis
ce papier, beaucoup de corrections ont été apportées aux implémentations
standards de \`malloc\`, la gestion du tas reste un vecteur d'attaque puissant.

L'objectif de ce dépôt est de réécrire les fonctions suivantes sous un axe de
sécurité :

\`\`\`c
#ifndef _SECMALLOC_H
#define _SECMALLOC_H
#include <stddef.h>
void *malloc(size_t size);
void free(void *ptr);
void *calloc(size_t nmemb, size_t size);
void *realloc(void *ptr, size_t size);
#endif
\`\`\`
\`\`\`

#### Préliminaires

- Votre code doit respecter, au maximum, les règles de programmation pour le
	développement sécurisé de logiciels en langage C de l'ANSSI (notamment
	l'annexe E sur les conventions de codage et de nommage).
- Votre développement doit suivre le principe du Test Driven Development :
	complétez les fichiers de test fournis.
- Les tests servent de preuve de l'implémentation des fonctionnalités demandées.

#### Tests

- Le \`Makefile\` fourni compile et exécute les tests écrits avec Criterion
	(dans \`test/test.c\`).

#### Bibliothèque statique

- \`make clean static\` doit produire \`libmy_secmalloc.a\`.
- Cette bibliothèque est utilisée par les tests et donne accès aux fonctions/
	variables internes testées.

#### Bibliothèque dynamique

- \`make clean dynamic\` doit produire \`lib/libmy_secmalloc.so\`.
- La bibliothèque devra exporter comme symboles publics les fonctions
	équivalentes à l'allocateur C classique :

\`\`\`bash
$ nm libmy_secmalloc.so | grep " T " | grep -v my_ | cut -f3 -d' ' | sort
# sortie attendue :
calloc
free
malloc
realloc
\`\`\`

- En utilisant \`LD_PRELOAD\`, on peut forcer l'utilisation de vos fonctions
	d'allocation pour n'importe quel programme. Exemple :

\`\`\`bash
$ ls
test
$ ls ~/my_secmalloc/lib/libmy_secmalloc.so
libmy_secmalloc.so
$ LD_PRELOAD=~/my_secmalloc/lib/libmy_secmalloc.so ls
test
\`\`\`

Ce mécanisme permet de réaliser des tests end-to-end.

### 2. Objectif

Le projet vise à approfondir votre compréhension de :

- Système d'exploitation Linux
- Mécanisme de gestion mémoire
- Heap overflows

L'accent est sur la sécurité (détection, log, robustesse) plutôt que sur la
performance (optimisation mémoire / temps d'exécution).

#### Écrire un allocateur

L'écriture d'un allocateur n'est pas triviale : certaines fonctions usuelles
(\`printf\`, ...) et des mécanismes système (\`ld.so\`) peuvent utiliser
l'allocateur de base.

Pour vous familiariser, vous pouvez détourner \`malloc\` via \`dlsym\` :

\`\`\`c
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
void *malloc(size_t size)
{
		(void) size;
		printf("Avant le vrai malloc %zu\\n", size);
		void *(*m)(size_t) = dlsym(RTLD_NEXT, "malloc");


[... Documentation tronquée pour l'affichage ...]
`
};