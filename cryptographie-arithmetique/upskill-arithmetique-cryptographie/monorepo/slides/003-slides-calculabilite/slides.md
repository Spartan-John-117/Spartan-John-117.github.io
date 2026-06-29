---
theme: seriph
layout: cover
highlighter: shiki
drawings:
  persist: false
background: /david-latorre-romero-0tNF_mHm_Ls-unsplash.jpg
---

# Maths [SUPPRIME_2600]

Calculabilité

---
layout: intro
class: text-center
---

# Récapitulatif

---

# Ce qu'on a vu

- Fondations des mathématiques
  - Calcul des propositions
  - Calcul des prédicats
  - Axiomatique
  - Systèmes de déductions
  - Théorie des ensembles
  - Arithmétique
- Formalisation
  - Syntaxe et sémantique
  - Règles de substitution
  - Applicables de manière automatique: programmable

---

# Ce qu'on va voir

- Comment formaliser la notion de programme ?
  - Définir la notion de "calculable"
  - Représenter un programme par une entité mathématique

---
layout: intro
class: text-center
---

# Théorie de la calculabilité

---

# Formaliser le calculable

- Intuitivement, le calculable c'est ce qu'on peut calculer sur papier
  - Un algorithme
- Fonction calculable = fonction qu'on pourrait programmer
  - Fonction logique, répond oui ou non
    - Notion de décidabilité en un temps fini
  - Fonction arithmétique
    - Calcule des nombres en un temps fini
    - Calcule des suites de nombres
- Peut t-on représenter un processus de calcul par une entité mathématique ?
  - La boucle serait bouclée:
    - On a posé les fondations des mathématiques par le calcul mécanique basé sur des substitutions
    - On serait capable de représenter ce calcul par une entité mathématique

---

# Pourquoi formaliser le calculable ?

- Permet de formaliser la notion de problème résolvable par un algorithme
  - On parle de problème décidable algorithmiquement
- On peut également définir la complexité en temps et en espace d'un problème
  - Quel est le temps nécessaire pour trouver une solution à un problème ?
  - Quel est l'espace mémoire nécessaire pour trouver une solution à un problème ?
- On peut également formaliser mathématiquement les langages de programmation
  - Et donc raisonner dessus, donner des propriétés, trouver des failles
- On peut se demander si tous les modèles de calcul qu'on applique sont équivalent et ce qu'on peut représenter comme algorithmes avec
  - Est ce que le calcul par substitution est équivalent au calcul qu'on peut implémenter en C ?
  - Est ce que les langages fonctionnels sont équivalent aux langages impératifs ?
- Permet de répondre à certaines questions des fondements des mathématiques
  - Est ce que la sémantique mathématique est entièrement représentable par des processus de calcul ?

---

# Théorie de la calculabilité

- Un domaine de la logique mathématique et de l'informatique théorique
  - Objectif: identifier la classe des fonctions qui peuvent être calculées à l'aide d'un algorithme
- Algorithme = qui peut être executé à la main, ou programmé
  - Algorithme de l'addition en primaire, on le fait à la main, on peut le programmer
  - Algorithme de résolution d'une équation
- S'interesse au limites des ordinateurs
  - Est ce que toutes les fonctions sont calculables ?
  - Est ce que toutes les structures mathématiques sont calculable ?
    - Les suites de nombres entiers naturels ?
    - Les nombres réels par exemple ?

---

# Histoire: Les machines à calculer

- Première machine à calculer: la pascaline de Blaise Pascal (17eme siècle)
  - Permet addition, soustraction, multiplication, division
- Au 19eme siècle, Jacquard met au point un métier à tisser mécanique et programmable avec des cartes perforées
  - A l'origine des premiers programmes de calcul
- En 1821, Charles Babbage développe une machine à calculer destiné au calcul de polynômes
- En 1834, il la combine avec les cartes perforée de Jacquard pour construire la machine analytique
  - Contient une unité de controle, une unité de calcul, une mémoire et une entrée sortie
- Entre 1842 et 1843, Ada Lovelace travaille en collaboration avec Babbage et devient en quelque sorte la première programmeuse
  - Elle développe un algorithme permettant de calculer les nombres de Bernoulli avec la machine analytique
  - Elle montre que la machine est un calculateur universel programmable, ce qui pose les fondements de la notion de calculabilité

---

# Histoire: La formalisation

- En 1900 David Hilbert pose une liste de 23 problèmes non résolu en maths. Le dixième s'énonce:
  - « On se donne une équation diophantienne à un nombre quelconque d'inconnues et à coefficients entiers rationnels : On demande de trouver une méthode par laquelle, au moyen d'un nombre fini d'opérations, on pourra distinguer si l'équation est résoluble en nombres entiers rationnels. »
    - On parle ici d'un problème de décision: étant donné une telle équation (l'entrée), on veut répondre "l'équation à une solution" (oui) ou "l'équation n'a pas de solution" (non) en un nombre fini d'étape.
    - "un nombre fini d'opérations": on cherche un algorithme. A cette étape il n'y a pas de définition formelle précise de ce qu'est un algorithme.
- C'est également l'époque de la crise des fondements.
  - Peut toujours démontrer un formule ou son contraire dans un système axiomatique ?
  - Godel à montré que pour toute théorie axiomatique non contradictoire de l'arithmétique, il existe des énoncés vrais qui ne sont pas démontrables dans cette théorie.
  - Il est également possible de le démontrer via la calculabilité, car les méthodes de déduction sont des processus algorithmiques

---

# Les grand modèles de calculabilité

- Les plus connus:
  - Machines de Turing
  - Lambda-calcul de Church
  - Fonctions récursive de Godel
- Les autres:
  - Machine à compteurs
  - Automates Cellulaires
  - Circuits booléens
  - Random access machines
  - ...
- Thèse de Church: la notion de fonction calculable ne dépend pas du formalisme choisit pour la modéliser

---

# Fonction calculable

- Intuitivement, une fonction $f(x)$ est calculable s'il existe une méthode précise qui étant donné un argument $x$ permet d'obtenir $f(x)$ en un nombre fini d'étapes
  - Par exemple, l'addition des nombres entier naturel est calculable puisque je peux le faire en appliquant l'algo de l'addition
  - Méthode de calcul défini par des moyens finis
- Thèse de Church: « N'importe quel moyen raisonnable de formaliser la notion d'« algorithme » est, en fait, équivalent à la notion de machine de Turing »
  - On dit qu'un langage de programmation est Turing-Complet quand il permet d 'implémenter l'ensemble des fonctions calculable
- Est ce que toutes les fonctions sont calculable ?

---

# Nombre calculable

- Un nombre réel est dit calculable si son expression décimale est énumérable via un algorithme
  - $1/3$ est calculable
    - Son expression décimale est "0.3333...". La répétition de "3" à l'infini est implémentable.
  - $\pi$ est calculable, on peut écrire un algorithme qui énumère toutes les décimales
- On autorise l'algorithme à s'executer indéfiniment, mais chaque décimale peut être atteinte en un nombre fini d'étapes
- Est ce que tous les nombres réels sont calculable ?

---

# Problème de l'arrêt

- Il n'existe pas de programme universel qui prenne n'importe quel programme en argument et qui, en temps fini, renvoie « oui » si l'exécution du programme reçu en argument finit par s'arrêter et « non » s'il ne finit pas.
- Se démontre via l'argument diagonal de Cantor

---

# Problème de la décision

- Peut t-on déterminer de façon mécanique si un énoncé est un théorème de la logique des prédicat munit de l'égalité ?
  - Théorème d'incomplétude: si la théorie est trop puissante (peut représenter l'arithmétique), alors non
- Peut également se démontrer via les limites sur les modèles de calcul
  - Si mon modèle de calcul est trop puissant (Turing-Complet), il engendre des processus trop complexes pour pouvoir s'auto-analyser

---
layout: intro
class: text-center
---

# Machines de Turing

---

# Introduction

- Modèle abstrait du fonctionnement d'un ordinateur
- Modèle impératif de calcul: on donne des ordres à la machine
- Très utilisé en informatique théorique pour définir la complexité algorithmique et les classes de problèmes
- L'objectif d'une MT est de modéliser mathématiquement le travail d'un humain (ou d'une machine) pour résoudre un problème donné
  - On lui donnerait une genre de recette et il execute la recette
  - Comme un algorithme qu'on programme
  - La MT est la recette

---

# Définition informelle

- Un ruban infini de cases. Ce ruban représente la mémoire de la machine. Chaque case contient un symbole d'un alphabet fini donné.
- Une tête de lecture/écriture se déplaçant sur le ruban.
- Un ensemble fini d'états, un état courants, un état initial, des états finaux
- Un graphe de transition entre états indiquant, en fonction de l'état courant et du symbole courant, quel symbole écrire et dans quelle direction se déplacer.

<div class="bg-color-white">

![](/machine-de-turing.jpg)

</div>

---

# Définition formelle

- Une machine de Turing déterministe est un quintuplet $(Q, \Gamma, q_{0}, \delta, F)$ tel que:
  - $Q$ est un ensemble fini d'états
  - $\Gamma$ est l'alphabet des symboles du ruban, contenant un symbole particulier $0 \in \Gamma$ représentant le vide.
  - $q_0 \in Q$ est létat initial
  - $\delta$ est la fonction de transition
    - On note $\delta: Q \times \Gamma \rightarrow Q \times \Gamma \times \{ \leftarrow, \rightarrow \}$, ce qui indique que $\delta$ prend ses arguments dans $Q \times \Gamma$ et donne des valeurs dans $Q \times \Gamma \times \{ \leftarrow, \rightarrow \}$
    - $Q \times \Gamma$ est l'ensemble des paires $(q, s)$ ou $q \in Q$ est un état et $s \in \Gamma$ est un symbole
    - $Q \times \Gamma \times \{ \leftarrow, \rightarrow \}$ est l'ensemble des triplets $(q', s', d)$ ou $q' \in Q$ est un état, $s' \in \Gamma$ est un symbole et $d \in \{ \leftarrow, \rightarrow \}$ une direction
    - $\delta(q, s)$ nous donnera donc un triplet $(q', s', d)$ indiquant: "si l'état courant est $q$ et le symbole lu est $s$ alors la machine passe dans l'état $q'$, écrit le symbole $s'$ et se déplacer dans la direction $d$.
  - $F \sube Q$ est l'ensemble des états finaux de la machine

---

# Fonctionnement

- Pour faire "tourner" une machine de Turing, on va lui donner en entrée un mot écrit sur le ruban et executer ses transitions une à une
  - Le mot est constitué de symboles de l'alphabet $\Gamma$
  - L'infinité des autres case est considéré contenir le symbole vide $0$
- Pour savoir quoi faire on utilise la fonction de transition. L'état initial est $q_0$ et la MT commence son execution sur la case contenant le premier symbole du mot d'entrée. Si ce symbokle est $s$, on va regarder $\delta(q_0, s)$ qui nous donnera un triplet $(q', s', d)$
  - $q'$ devient le nouvel état
  - On écrit $s'$ à la place du premier symbole du mot d'entrée
  - On se déplace à gauche si $d = \leftarrow$, à droite si $d = \rightarrow$
- On recommence tant qu'on arrive pas dans un état final
  - Une machine de Turing peut tourner à l'infini si elle n'arrive jamais dans un état final
  - Si elle s'arrete dans un état final on considère que la sortie de la MT est le mot écrit sur le ruban
- Le nombre d'état et de symbole est fini, on peut donc représenter $\delta$ par une table de transitions

---

# Exemple: doubler le nombre de '1'

- L'objectif est de construire une machine qui double le nombre de 1 de l'entrée en séparant d'un symbole vide.
  - Exemple: $111$ devient $1110111$
- On pose $\Gamma = \{ 0, 1 \}$, $Q = \{ e_1, e_2, e_3, e_4, e_5, e_6 \}$, $q_0 = e_1$

<div class="flex place-items-center ">

![](/transitions.png)

![](/execution.png)

</div>

---

# Exemple: calculer un tiers en binaire

- L'objectif est de construire une machine qui écrit l'infinité des décimales de $1/3$ en binaire
  - C'est à dire $010101010101...$ représentant $0,010101010101..$
  - Cette machine ne termine donc jamais, mais donne l'exemple d'un nombre réel calculable
- On pose $\Gamma = \{ 0, 1 \}$, $Q = \{ a, b \}$, $q_0 = a$

<div class="flex place-items-center space-x-8">

![](/transitions-tiers.png)

![](/execution-tiers.png)

</div>

---

# Remarques

- Les machines de Turing c'est le bas niveau du bas niveau
  - Plus bas niveau que de l'assembleur
- Les machines de Turing c'est fastidieux à écrire et executer
  - Difficile de trouver l'algorithme pour un problème donné
- C'est donc un objet principalement conceptuel
  - L'objectif est d'utiliser la définition formelle des machines de Turing pour démontrer des résultats de calculabilité
- Mais on peut quand même s'amuser un peu: https://turingmachine.io/

---

# Machines de Turing Universelle

- Une MT universelle est une MT qui peut simuler n'importe quelle machine de Turing sur n'importe quelle entrée
  - Autrement dit, une MT universelle est un interpreteur: on lui donne un programme, une entrée, et elle execute ce programme
- Pour cela on encode la definition de la MT à executer dans un alphabet compris par la MT universelle
  - On peut utiliser l'alphabet qu'on veut tant qu'on sait écrire la MT universelle qui l'executera
  - On peut utiliser un alphabet binaire
    - comme un processeur prendrait en entrée des instructions qui ont été compilés en binaire, une MT universelle pourrait prendre la description des transitions et des états "compilés" dans un alphabet binaire
- On écrit l'encodage de la MT a executer sur le ruban, suivi d'un symbole de séparation, suivi de l'entrée sur laquelle executer la machine
  - Toute cette écriture constitue l'entrée complète de la MT universelle

---

# Machines de Turing Universelle

<div class="bg-white">

![](/MT_universelle.png)

</div>

---

# Rapport entre logique et machines de Turing

- Turing montre qu'il est possible de construire une machine de Turing universelle
  - On ne va pas le faire ici
- A partir d'une telle machine, on peut manipuler d'autres machines de Turing
  - On peut donc manipuler les entités de notre formalisme dans le cadre du formalisme qui est décrit
  - Un peu comme en méta-mathématique on cherche à manipuler les démonstrations comme des élements du cadre qu'on est en train de définir
- Ce rapport très étroit amène Turing à donner des démonstrations analogue au théorème d'incomplétude de Godel, mais dans le formalisme des machines de Turing
  - A nouveau, on observe qu'un formalisme mécanique n'est pas suffisant pour représenter tout la sémantique mathématique

---

# Rapport entre machines de Turing universelle et Ordinateurs

- La première machine programmable est la machine analytique de Babbage
  - Mais elle se programme avec les cartes de métier à tisser de Jacquard, un objet non modifiable donc
- La MT universelle introduit une idée fondamentale: on peut stocker un programme en mémoire, l'executer, et même le modifier
  - Une MTU pourrait donc changer sa table de transition pendant son execution et se reprogrammer
  - Donne une première idée de l'intelligence artificielle informatique
  - Application concrète: la compilation just in time
- En 1945 Turing publie le premier article décrivant la conception d'un ordinateur à l'architecture d'aujourd'hui (architecture de von Neumann).
  - La machine physique associée (EDVAC) sera opérationelle en 1951
  - Avant cela en 1948 le SSEM de l'université de Manchester sera le premier ordinateur électronique executant un programme enregistré en mémoire (considéré comme un proof of concept)

---

# Problème de l'arrêt

- Est t-il possible de détérminer si un programme s'arrête sur une entrée par la seule analyse de son code ?
- Dans le formalisme des machines de Turing, existe t-il une machine de Turing prenant en entrée le codage d'une machine de Turing $M$, une entrée $e$, qui écrit $0$ sur son ruban si $M$ s'arrête sur l'entrée $e$ et qui écrit $1$ sur son ruban si $M$ boucle à l'infini sur l'entrée $e$.
- Autrement dit: peut-on detecter algorithmiquement si un programme boucle à l'infini ?

---

# Indécidabilité du problème de l'arrêt

- On peut montrer par l'absurde qu'une telle machine n'existe pas
- Pour simplifier on donne la démonstration avec du pseudo-code (qu'on pourrait convertir en machines de Turing, mais ce n'est pas necessaire)
- On assimile les MT à des fonctions prennant en entrée un mot fini `m` sur un alphabet fini (le contenu du ruban au début de l'execution)
  - Une fonction est elle même un mot fini: son code

---

# Démonstration par l'absurde

- Supposons qu'il existe une fonction `halt(prog, m)` qui décide le problème de l'arrêt.
  - Si `prog(m)` s'arrête, alors `halt(prog, m)` renvoit `1`
  - Si `prog(m)` boucle à l'infini, alors `halt(prog, m)` renvoit `0`
- On construit alors le fonction suivant:

```
def diagonale(prog):
  if halt(prog, prog) == 1:
    while true: pass
  else:
    return 1
```

- On obtient une contradiction dans la définition de `diagonale` en l'executant sur son propre code en appelant `diagonale(diagonale)`:
  - Si `halt(diagonale, diagonale)` on passe dans le if: `diagonale(diagonale)` doit boucler. Mais `halt(diagonale, diagonale)` vaut 1 précisément si `diagonale` s'arrete !
  - Sinon on passe dans le else: `diagonale(diagonale)` renvoit 1, donc `diagonale(diagonale)` s'arrête, et `halt(diagonale, diagonale)` renvoit 1, on aurait du passer dans le if !

---

# Rapport entre problème de l'arrêt et calcul infini

- Le problème de l'arrêt nous indique qu'il est impossible d'analyser le comportement précis d'un algorithme infini en examinant uniquement son code fini
- La complexité du comportement engendré dépasse la finitude de la réprésentation sous forme de code
- A des implications sur l'analyse de programmes en informatique: on sait que certaines choses sont tout simplement impossible à determiner

---

# Machines de Turing non deterministe

- On a vu les machines de Turing deterministes
  - Etant donné un état et un symbole lu, on ne peut aller que dans un seul état et écrire un seul nouveau symbole
  - L'execution d'une MTD peut donc être décrite par une séquence de transitions d'état et d'évolution du ruban
- On peut également définir les machines de Turing non deterministes
  - Un état peut mener à plusieurs états
  - On "imagine" que le calcul se fait par une exploration en parallèle
  - L'execution d'une MTND peut donc être décrite par un arbre de transitions d'état et évolution du ruban
  - Le temps de calcul est considéré comme étant la taille de la branche la plus courte acceptant une entrée
- Etant donné une MTND, on peut toujours construire une MTD effectuant le même calcul (il suffit de faire une exploration en largeur de l'arbre des transitions)
- Utile en théorie de la complexité, pour définir la classe des problème NP qu'on peut résoudre en temps polynomial via une MTND

---

# Illustration MTND

<div class="bg-color-white">

![](/mtnd.png)

</div>

---

# Problèmes de décision

- Intuitivement, un problème de décision est une question mathématique dont la réponse est soit oui soit non
  - Peut donc se formaliser comme l'évaluation d'une formule d'un système formel
  - Dans le cadre de la calculabilité, cette formule à une entrée, c'est donc une fonction
- On dit qu'un problème de décision est décidable s'il existe une machine de Turing qui implémente l'algorithme permettant de calculer la décision pour une entrée donnée
  - Une MT qui se termine et donne la réponse attendue
  - Si ça n'existe pas, le problème est dit indécidable
  - Décidable signifie "calculable"
- Exemple de problème indécidable: le problème de l'arrêt
- Exemple de problème décidable: determiner si un nombre entier est premier

---

# Problèmes de calcul

- Un problème de calcul consiste à implémenter une fonction mathématique
- Une suite mathématique correspond à une fonction entière: on lui donne un nombre entier en entrée, elle fournit un nombre entier en sortie
  - Exemple: $u_n = 2n$, qu'on peut aussi écrire $f(n) = 2n$

---

# De la décision au calcul

- On peut construire un problème de décision à partir d'une fonction
  - Exemple: Si $f(n) = 2n$, on pose le problème de décision qui prend en entrée un couple $(a, b)$ et répond oui si $b = 2a$, non sinon.
  - Cela revient à identifier une fonction $f$ à son graphe, l'ensemble des couple $(a, b)$ qui vérifie la proposition $b = f(a)$
  - Souvenez vous mes prédicats $deux(x)$, $succ(x, y)$, c'est exactement ce qu'ils faisait: exprimer le résultat d'un calcul par un filtre
- Si ce problème de décision est décidable, alors la fonction associée est calculable:

```
def f(a):
  b = 0
  while True:
    if decision_problem(a, b) == 1:
      return b
    b += 1
```

- C'est exactement comme ça qu'on peut implémenter la fonction d'énumération des nombres premiers

---

# Est ce que toutes les fonctions sont calculables ?

- On peut se poser la question: est ce que toutes les fonctions entières sont calculables ?
- Non, car il y a plus de fonctions entières que de machines de Turing

---

# Combien y-a t-il de machines de Turing ?

- Une infinité, mais quelle infinité ?
- Une MT c'est un programme fini, qu'on peut identifier à son code source
- Un code source fini s'experime avec des symboles, qu'on peut encoder en binaire
- Une séquence binaire finie peut être identifiée à un nombre entier naturel
- On a donc "autant" de MT que de nombres entiers naturels

---

# Combien y-a t-il de de fonctions entières ?

- Il y a plus de fonctions entières que de nombres entiers
  - On dit que l'ensemble des fonctions entières n'est pas dénombrable, ou énumérable
- Supposons qu'on puisse énumérer les fonctions entières
  - On peut donc associer un entier $i$ à chaque fonction entière $f$, on peut la renommer $f_i$
  - On construit la fonction $g(n) = f_n(n) + 1$
  - $g$ est une fonction entière, on doit donc pouvoir trouver $i$ tel que $\forall n, g(n) = f_i(n)$
  - Mais par définition, $g(n) = f_n(n) + 1$, donc $g(i) = f_i(i) + 1 \neq f_i(n)$
  - Donc on ne peut pas énumérer les fonctions entières (c'est un argument diagonal, comme celui utilisé pour démontrer que le problème de l'arrêt n'est pas décidable)
- Il y a donc plus de fonctions entières que d'entiers naturels, donc plus de fonctions entières que de machines de Turing
  - Exemple de fonction non calculable, mais parfaitement définit: fonction du Castor affairé
    - Parfaitement définie syntaxiquement
    - Non calculable par un algorithme

---

# Est ce que tous les nombres réels sont calculable ?

- Un nombre réel $x \in [0, 1]$ est calculable s'il existe une MT qui enumère l'ensemble de ses décimales
- Avec un argument diagonal on montre qu'il y a plus de nombres réels que de nombres entiers, donc de MT
- Conclusion: la majorité des nombres réels ne sont pas calculable

---
layout: intro
class: text-center
---

# Autres formalisations des fonctions calculables

---

# Les fonctions récursives de Godel

- En informatique, les fonctions récursives sont des fonctions dont le calcul nécessite d'invoquer la fonction elle-même
- En théorie de la calculabilité, une fonction récursive est une fonction à un ou plusieurs arguments entiers, qui peut se calculer en tout point par une procédure mécanique
- Une fonction récursive primitive est une fonction construite à partir de la fonction nulle, de la fonction successeur, des fonctions projections et des schémas primitifs de récursion et de composition.
  - C'est ce qu'on a fait à la première session pour définir l'addition et la multiplication
      - $addition(0, y) = y$
      - $addition(succ(x), y) = succ(addition(x, y))$
  - Cette définition ne "capture" pas toutes les fonctions calculable (exemple: fonction d'Ackerman)
- La récursivité mécanique correspond bien à la notion de calculable

---

# Le lambda-calcul

- En lambda calcul on représente toute par des fonctions qu'on combine par application
- Les fonctions sont représentées par des expressions de la forme $\lambda x.E$ ou $E$ est une expression contenant le symbole $x$
  - La fonction identité: $\lambda x.x$
  - La fonction constante valant y: $\lambda x.y$
- Pour représenter l'application d'une fonction, on concatène: $F E$ représente l'évaluation de $F$ sur l'expression $E$
  - Evaluer c'est simplement substituer la variable.
  - $(\lambda x.x) (\lambda x.y) = \lambda x.y$
- On construit des fonctions à plusieurs variables en construisant des fonctions qui renvoient des fonctions:
  - $\lambda z. (\lambda x. (\lambda y. (z y) x))$
- Church montre que cette construction permet de formaliser des calculs au sens qu'on l'entend en algorithmique

---

# La thèse de Church

- Church montre que ces formalisations sont équivalentes: elles permettent de définir la même classe de fonctions mathématiques, qu'on appelle les fonctions calculable
  - Pour cela il montre qu'on peut transformer une MT en fonction récursive, et inversement
  - Pareil pour passer au lambda-calcul
- Remarque:
  - Les formalismes de fonctions récursive et lambda-calcul sont à la base des langages de programmation fonctionelle
    - Haskell, Ocaml
    - Utilise une notion de calcul "pur", sans état: l'état courant du calcul est directement encodé dans le méchanisme de substitution, via une pile implicite
  - Le formalisme des machines de Turing correspond plutot à la programmation impérative
    - Formalise directement la transition entre états et d'effet de bord (écriture sur le ruban)

---

# Formalismes plus faible

- On a des formalismes de calcul plus faible en mathématiques, qui ne sont pas Turing-Complet (ne représente pas toutes les fonctions calculables)
- Exemple: les automates finis en théorie des langages
  - Permet de calculer des problèmes de décision sur la reconnaissance de mots dans une syntaxe donnée
  - Exprime les langages réguliers: les ensembles de mots qui respectent une expression régulières (regexpr)
- Permet des modèles plus simples de calcul, donc plus efficace
- Permet des modèles plus restreints de calcul, donc moins hackable, et mieux analysable

---
layout: intro
class: text-center
---

# Complexité

---

#  Théorie de la complexité

- A partir du formalisme des MT, on peut définir la notion de complexité d'un problème calculable
- Complexité: évaluation du cout de résolution d'un problème
  - Cout en temps: nombre d'étapes nécessaire pour le résoudre
  - Cout en espace: nombre de cases du ruban utilisés pour le résoudre
- La complexité dépend généralement de la taille de l'entrée, c'est à dire le nombre de case utilisées par l'entrée
  - Si on note cette taille $n$, on peut dériver une formule qui dépend de $n$ et qui évalue précisément la complexité d'une machine de Turing
- La complexité d'un problème est définie comme le minimum de la complexité de toutes les MT qui résolvent ce problème
  - En gros: le cout de l'algorithme le plus efficace

---

# Comportement asymptotique

- Une MT qui parcourt son entrée de gauche à droite et s'arrete au premier symbole blanc effectue $n$ opérations
- Une MT qui parcourt de gauche à droite et revient effectue $2n + 1$ opérations
  - Le $+1$ correspond au fait de revenir du symbole blanc au dernier symbole de l'entrée
- On dit que ces deux MT ont la même classe de complexité: linéaire
  - Linéaire signifie que la formule qui évalue la complexité à pour forme $an +b$ (c'est une droite)
  - Si on double la taille de l'entrée, alors le cout double
  - On note $O(n)$ pour englober toutes les formules de complexité linéaire

---

# Comportement asymptotique

- Ce qui nous interesse c'est le comportement asymptotique d'un algorithme: si la taille de son entrée tend vers l'infini, vers quelle forme tend sa fonction de cout
- On distingue la complexité polynomiale: $O(n)$, $O(n^2)$, $O(n^k)$
  - Exemple de MT en $O(n^2)$: une MT qui parcourt son entrée, et pour chaque case reparcourt son entrée (la double boucle imbriqué)
- Complexité constante: $O(1)$
  - Un nombre d'opérations qui ne dépend pas de la taille l'entrée
- Complexité logarithmique: $O(log(n))$
  - Exemple: recherche tableau trié, calcul de puissance
- Complexité exponentielle: $O(k^n)$
  - Exemple: SAT, problème du voyageur de commerce


---

# Classes de complexité

- On peut classer les problèmes en fonction des algorithmes connu pour les résoudre
- La classe $P$ est la classe des problèmes dont on connait une MT deterministe capable de le résoudre en temps polynomial
- La classe $NP$ est la classe des problèmes dont on connait une MT non deterministe capable de le résoudre en temps polynomial
- A ce jour on ne sait toujours pas si $P = NP$
- On a des problèmes dit $NP$-complet: on sait construire en temps polynomial sur une MT deterministe une conversion de n'importe quel problème $NP$ en un $NP-complet
  - Il suffirait de montrer qu'un problème $NP$-complet est dans $P$ pour montrer que $P = NP$, et inversement
  - 1M à la clef

---

# Complexité en pratique

- En pratique on évalue la complexité sur des algorithmes exprimés en code ou pseudo-code
- On verra demain des méthodes de calcul de la complexité d'un algorithme
