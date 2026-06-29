---
# try also 'default' to start simple
theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: /jose-campos-zRkBOOpKRhs-unsplash.jpg
# apply any windi css classes to the current slide
class: 'text-center'
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# show line numbers in code blocks
lineNumbers: false
# persist drawings in exports and build
drawings:
  persist: false
# use UnoCSS
css: unocss
---

# Maths [SUPPRIME_2600]

---

# Objectifs pédagogiques

- Déconstruire des concepts mathématique de base
  - Qu'est ce qu'un nombre ? comment ça se définit ? Comment ça se manipule ?
  - Distinction sémantique et syntaxique; conceptuel vs mécanique
  - Comprendre l’aspect très algorithmique des maths « bas niveau »
  - Exploration par le code
- Logique, Calculabilité, Algorithmique
  - Comment formalise t'on la notion de calcul, et donc l'informatique et l'algorithmique ?
  - Quel outils mathématiques pour analyser des programmes
    - Prouver leur validité
    - Calculer leur cout
    - Définir ce qui est calculable ou non
- Exemple pratique d'application des mathématiques en informatique & sécurité
  - Cryptographie

---

# Intervenant: Laurent NOËL

- Mail: laurent.noel.c2ba@gmail.com
  - laurent.noel@ecole[SUPPRIME_2600].com
- Discord: c2ba
- Background:
  - Recherche et développement 3D, spécialisé en synthèse d'images, développement de moteurs 3D
  - Développement full-stack, cloud & infra
  - Développement blockchain, crypto-monnaies, tokenomics, finance décentralisée et trading algorithmique

---
layout: cover
---

# Maths [SUPPRIME_2600]

Représentation et formalisation des nombres

---
layout: intro
class: text-center
---

# Le concept de nombre

---

# La formalisation

- Une obscession des mathématiciens est de s'assurer de la cohérence logique de l'ensemble des maths
- Il est plus simple de s'assurer de la cohérence en partant de concepts et bases très simples
- Base très simple =
  - Faisable à la main par un humain sur papier
  - Mécanique, executable en appliquant des règles sans avoir à réflechir
- Si les règles qu'on se donne sont simples et nous semblent cohérentes, on considerera qu'un enchainement d'application de ces règles est cohérent également
  - Une règle plus complexe doit correspondre à l'application successive de règles plus simples
  - Ces règles complexes seront des propriétés, théorèmes, algorithmes, règles de calcul
  - Construire l'edifice mathématique, c'est découvrir de nouvelles règles cohérentes à partir de règles qu'on connait déjà
- On va donc formaliser les nombres et opérations sur ces nombres via des règles simples et applicables mécaniquement
  - Dans ce cadre, le calcul numérique (addition, multiplication, ...) est déjà "complexe"

---

# Qu’est ce qu’un nombre ?

- Représente le concept de quantité d’objets
  - 0 =
  - 1 = 🍎
  - 2 = 🍎🍎
  - ...
  - 8 = 🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎
- On peut les représenter de différentes manières
  - La notation en pommes (pas de pomme, une pomme 🍎, deux pommes |🍎🍎, ...)
  - La notation « classique » en base 10: 0, 1, 2, ..., 11, 12, ..., 10478, ...
- On les appelle les **nombres entiers naturels**

---

# Formaliser une définition de nombre entier

- Comment définir les nombres entier ?
  - On cherche à préciser la définition intuitive "nombre d'objets"
  - On veut une définition syntaxique: une règle de construction permettant de construire tous les nombres entier
- Exemple avec les pommes
  - avec le symbole 🍎, je peux construire le nombre 1
  - Partant du nombre 1, je peux construire le nombre 2 en ajoutant une pomme devant:
    - 🍎 -> 🍏🍎
  - Je peux répéter autant de fois que je veux, pour construire:
    - 🍎🍎 -> 🍏🍎🍎
    - 🍎🍎🍎 -> 🍏🍎🍎🍎
    - ...
- On remarque la propriété fondamentale suivante:
  - Un entier naturel à toujours un unique entier qui le suit, son « successeur »

---

# Règles de construction des nombres entier

- On définit les nombres entiers naturels par:
  - L’élément appelé "zéro" et noté $0$ est un entier naturel
  - Tout entier naturel $n$ a un unique successeur, noté $Sn$ qui est un entier naturel.
- En language mathématique on note:

$$
0 \in \N \\
n \in \N \implies Sn \in \N
$$
- La première ligne se lit "$0$ appartient à $\N$, où $\N$ réprésente l'ensemble des entiers naturel
- La deuxième ligne se lit "si $n$ appartient à $\N$, alors $Sn$ appartient à $\N$"

---

# Exemple et comparaison avec les pommes

- Par définition, "L’élément appelé zéro et noté $0$ est un entier naturel"
  - Cela réprésente "pas de pommes"
- Par définition, "Tout entier naturel $n$ a un unique successeur, noté $Sn$ qui est un entier naturel."
  - Or $0$ est un entier naturel
  - En prenant $n = 0$, on a $Sn = S0$, le successeur de $0$
  - Il représente le nombre « un »
  - ou une pomme 🍎
- Puisque $S0$ est un entier naturel:
  - En prenant $n = S0$, on a $Sn = SS0$, le successeur de $S0$
  - Il représente le nombre « deux »
  - ou deux pommes 🍎🍎
- $SSS0$, $SSSS0$, $SSSSS0$, … sont des entiers naturels
  - Tout comme 🍎🍎🍎, 🍎🍎🍎🍎, 🍎🍎🍎🍎🍎

---

# L'opérateur successeur

- Ajouter un $S$, c'est comme ajouter une pomme 🍎 devant, les règle version pommes:
  - Tout entier naturel $n$ a un unique successeur, noté 🍎$n$ qui est un entier naturel.
- Le $S$ s'appelle l'opérateur "successeur", il s'applique à un nombre $n$ pour donner son suivant $Sn$
- En terme de calcul « classique », l’opération $Sn$ correspond à faire $n + 1$
  - Mais on a pas encore définit l’opération $+$ !
- Ici on reste à un niveau syntaxique très mécanique
  - On part de $0$, et on ajoute des $S$ devant itérativement pour construire les autres nombres
  - La logique du $+$ n'existe pas encore dans notre univers
- Bien comprendre ici qu'on cherche à définir une opération minimale pour construire une représentation des nombres entier
  - L'ajout de $S$ pour construire les nombres, c'est vraiment comme représenter "un nombre d'objets", des $S$ en l'occurence, mais ça pourrait être n'importe quoi.

---

# TP: coder en python l'opérateur successeur

- Suivez les instructions du README du repo https://gitlab.com/maths-[SUPPRIME_2600]/monorepo pour la mise en place de l'environnement de développement du cours
- Les premiers exercices sont des fonctions à coder dans `apps/tp-nombres/src/tp_nombres/__init__.py`
- Ecrire une fonction `nombre_entier(n: int) -> str` qui pour un nombre entier $n$ donné nous renvoie sa représentation avec des $S$. Examples:
  - `nombre_entier(0) == "0"`
  - `nombre_entier(1) == "S0"`
  - `nombre_entier(7) == "SSSSSSS0"`
- Ecrire une fonction `S(n: str) -> str`  qui calcule le successeur d'un nombre. Examples:
  - `S("0") == "S0"`
  - `S("S0") == "SS0"`
  - `S("SSSSSSS0") == "SSSSSSSS0"`

---

# Définir des opérations

- La **substitution** comme mécanisme fondamental
  - Une règle de substitution s'écrit sous la forme $x \rightarrow y$
  - Elle indique que j'ai le droit de remplacer $x$ par $y$
  - D'un point de vue mécanique, cela indique "si je vois $x$, je peux mettre $y$ a la place et continuer d'autres substitution"
- On va définir l’addition, la multiplication et l’exponentiation simplement par substitution
  - Pas de "calcul" au sens commun (numérique)
  - Du "calcul" algorithmique, des suites de substitutions, que l'on peut faire mécaniquement sur papier, on que l'on peut coder
- Le processus est toujours le même et se fait récursivement:
  - On définit la substitution en zéro (point de départ)
  - On définit récursivement l’opération pour le successeur d’un nombre quelquonque

---

# Définir l'addition $+$

- Reprenons les pommes, intuitivement des règles de substitutions traduisant l'additions seraient:
  - 🍎🍎🍎 + 🍎🍎  $\rightarrow$ 🍎🍎🍎🍎🍎
  - 🍎 + 🍎 $\rightarrow$ 🍎🍎
  - 🍎🍎🍎🍎 + 🍎 $\rightarrow$ 🍎🍎🍎🍎🍎
- On comprend qu'il existe une infinité de règles valides, c'est la table d'addition à une infinité de ligne et colonne, on ne peut pas tout énumérer !
- Peut on trouver un nombre fini de règles de substitutions qui permettent de construire l'infinité des règles d'addition possibles ?
  - Par itération de substitutions
- 🍎🍎🍎 + 🍎🍎 $\rightarrow$ 🍎 (🍎🍎 + 🍎🍎) $\rightarrow$ 🍎🍎 (🍎 + 🍎🍎) $\rightarrow$ 🍎🍎🍎( + 🍎🍎) $\rightarrow$ 🍎🍎🍎🍎🍎
  - 2 règles:
    - 🍎$n$ + $x$ $\rightarrow$ 🍎$(n + x)$
    - $+ x$ $\rightarrow x$

---

# Définir l'addition $+$

- Dans notre cas, les entiers peuvent être de deux formes seulement:
  - $0$ est un entier
  - Si $n$ est un entier, $Sn$ est un entier
- On va donc définir, par substitution, a quoi correspond $0 + x$ et $Sn + x$, ou $x$ est un entier
  - Le premier est facile $0 + x \rightarrow x$
- Le deuxième est plus compliqué, on voudrait pouvoir écrire $Sn + x \rightarrow Snx$
  - Mais $nx$ ne veut rien dire dans notre language, on ne peut pas "concaténer" deux variables
  - Pourquoi ? Imaginons que $n = SSS0$ et $x = S0$, alors $nx = SSS0S0$, ce n'est pas un nombre entier valide synatiquement
- Par contre, on peut additionner, puisqu'on est en train de définir l'addition !
  - Une concaténation, finalement c'est une addition
  - Donc $nx$ c'est plutot $n + x$
  - $Sn + x \rightarrow S(n + x)$

---

# Définir l'addition $+$

- Nos règles:
  1. $0 + x \rightarrow x$
  2. $Sn + x \rightarrow S(n + x)$
- Une machine peut elle vraiment appliquer ça ? Essayons avec l'addition $SS0 + SSS0$ (2 + 3 = 5)
  - On veut substituer $SS0 + SSS0$, c'est de la forme $Sn + x$ avec $n = S0$ et $x = SSS0$
    - On applique la règle 2: $SS0 + SSS0 \rightarrow S(n + x) \rightarrow S(S0 + SSS0)$
    - On observe l'apparition d'une autre addition: $S0 + SSS0$, on recommence:
  - On veut substituer $S0 + SSS0$, c'est de la forme $Sn + x$ avec $n = 0$ et $x = SSS0$
    - On applique la règle 2: $S0 + SSS0 \rightarrow S(n + x) \rightarrow S(0 + SSS0)$
  - On veut substituer $0 + SSS0$, c'est de la forme $0 + x$ avec $x = SSS0$
    - On applique la règle 1: $0 + SSS0 \rightarrow SSS0$, fin de la récursion !
- $SS0 + SSS0 \rightarrow S(S0 + SSS0) \rightarrow S(S(0 + SSS0)) \rightarrow S(S(SSS0)) \rightarrow SSSSS0$
- 🍎🍎 + 🍎🍎🍎 $\rightarrow$ 🍎 (🍎 + 🍎🍎🍎) $\rightarrow$ 🍎(🍎 ( + 🍎🍎🍎)) $\rightarrow$  🍎(🍎(🍎🍎🍎)) $\rightarrow$ 🍎🍎🍎🍎🍎

---

# TP: coder en python l'addition

- Ecrire une fonction `addition(a: str, b: str) -> str`. On veut par exemple:
  - `addition("SS0", "SSS0") == "SSSSS0"`
  - `addition("0", "SS0") == addition("SS0", "0") == "SS0"`
- Algorithme:
  - On veut reproduire nos règles
    1. $0 + x \rightarrow x$
    2. $Sn + x \rightarrow S(n + x)$
  - `a` c'est soit $0$ soit $Sn$, `b` c'est $x$
  - Donc, si `a == "0"` on traduit en python la premiere règle
    - $\rightarrow x$
    - `return b`
  - Sinon, si `a.startswith("S")` on traduit en python la deuxième règle
    - $\rightarrow S(n + x)$
    - `return S(addition(a[1:], b)) // S a déjà été codée plus haut`

---

# Définir la multiplication $\times$

- Multiplier c’est itérer l’addition
  - $n \times m$ c'est comme $m + m + ... + m$, $n$ fois
  - On voudrait écrire $n \times m \rightarrow m + m + ... + m$, mais la notation $+ ... +$ n'existe pas dans notre language (et est imprécise)
- On procède comme pour l'addition, on définie une règle pour $0 \times x$ et une règle pour $Sn \times x$
  - La première doit être cohérente avec l'idée qu'on se fait de la multiplication
  - La deuxième doit se transformer en $x + x + ... + x$ par itérations successive, avec $Sn$ termes
- Règles
  1. $0 \times x \rightarrow 0$
  2. $Sn \times x \rightarrow x + (n \times x)$
- Intuitivement, la deuxième règle extrait un $x +$, et l'application récursive sur $(n \times x)$ viendra extraire les autres $x +$
  - A la fin on aura bien $x + x + ... + x$

---

# Example de multiplication $\times$

- Règles
  1. $0 \times x \rightarrow 0$
  2. $S\blue{n} \times \green{x} \rightarrow (\blue{n} \times \green{x}) + \green{x}$
- $SS0 \times SSS0$ ($2 \times 3 = 6$)
  - $S\blue{S0} \times \green{SSS0} \rightarrow (\blue{S0} \times \green{SSS0}) + \green{SSS0}$ (règle 2 avec $\green{x = SSS0}$ et $\blue{n = S0}$)
  - $S\blue{0} \times \green{SSS0} \rightarrow (\blue{0} \times \green{SSS0}) + \green{SSS0}$ (règle 2 avec $\green{x = SSS0}$ et $\blue{n = 0}$)
  - $\blue{0} \times \green{SSS0} \rightarrow \blue{0}$ (règle 1 avec $\green{x = SSS0}$)
- On combine tout:
$$
SS0 \times SSS0 \rightarrow (S0 \times SSS0) + SSS0 \rightarrow ((0 \times SSS0) + SSS0) + SSS0 \rightarrow ((0) + SSS0) + SSS0
$$
- On fini avec une expression qui ne contient que des additions:
$$
((0) + SSS0) + SSS0 \rightarrow (0 + SSS0) + SSS0 \rightarrow SSS0 + SSS0 \rightarrow ... \rightarrow SSSSSS0
$$
- A la place des $\rightarrow ... \rightarrow$ on devrait executer la suite de substitutions des règles de l'addition

---

# TP: coder en python la multiplication

- Ecrire une fonction `multiplication(a: str, b: str) -> str`. On veut par exemple:
  - `multiplication("SS0", "SSS0") == "SSSSSS0"`
  - `multiplication("0", "SS0") == multiplication("SS0", "0") == "0"`
- On veut reproduire nos règles:
  1. $0 \times x \rightarrow 0$
  2. $S\blue{n} \times \green{x} \rightarrow (\blue{n} \times \green{x}) + \green{x}$
- Pas d'aide sur l'algorithme cette fois !
  - Pensez à réutiliser votre fonction `addition`

---

# Propriétés

- Une propriété est une égalité générale vraie
  - C'est a dire une certaine substitution qui peut s'obtenir quelque soit les valeurs des nombres
- Nous avons par exemple les propriétés suivantes:
  - Associativité: $(a \times b) \times c = a \times (b \times c) = a \times b \times c$
  - Associativité: $(a + b) + c = a + (b + c) = a + b + c$
  - Commutativité: $a + b = b + a$
  - Commutativité: $a \times b = b \times a$
  - Elément neutre: $a \times S0 = a$ (rappel: $S0$ c’est 1)
  - Distributivité: $a \times (b + c) = a \times b + a \times c$
- Ce sont des règles qu'on apprend en général au collège qui permettent de simplifier des calculs (et simplifier, c'est substituer pour réduire)
- En remplaçant $a$, $b$ et $c$ par n'importe quel nombre, et en appliquant nos algorithmes d'addition/multiplication, on constaterait que des propriétés sont vraies
- Mais comment démontrer formellement qu'elles sont tout le temps vraie ?

---

# Démonstration par principe de récurrence

- Je ne peux pas essayer pour tous les nombres entiers
  - Comment passer du fini à l’infini ?
  - On a déjà fait un passage du fini à l'infini par nos règles d'addition/multiplication
    - 2 règles permettent de faire une infinité d'additions
    - la mécanique était de définir une règle pour 0, et une règle recursive
    - On peut faire pareil pour démontrer une propriété
- Si une propriété $P$ est vraie pour 0 et qu’elle se « propage » d’un entier à son successeur, alors elle est vraie pour tous les entiers naturels
  - En logique propositionelle on écrit:
    - $(P(0)$ et $P(n) \implies P(Sn))$ $\implies$ $P(n)$ pour tout $n$
- Image des dominos
  - Si un premier domino tombe (propriété vraie pour 0)
  - Et que la chute d’un domino entraine la chute du suivant (propagation d'un entier à son successeur)
  - Alors tous les domino tombent (propriété vraie pour tous les entiers)

---

# Principe de récurrence et substitutions

- Dans le principe de récurrence se cache en réalité une infinité de substitutions
- En logique, écrire que $P(n) \implies P(Sn)$, cela signifie que je peux substituer $P(Sn)$ à $P(n)$ si $P(n)$ est vraie.
  - $P(n) \implies P(Sn)$ me permet ensuite d'appliquer $P(n) \rightarrow P(Sn)$ dans une suite de substitution
- Lorsqu'on applique le principe de récurrence:
  - On démontre que $P(0)$ est vraie, je peux donc écrire
    - $P(0)$ est vraie
  - On démontre que $P(n) \implies P(Sn)$ est vrai quelque soit $n$, donc pour $n = 0$ je peux substituer:
    - $P(0)$ est vraie $\rightarrow$ $P(S0)$ est vraie
  - Et pour $n = S0$ je peux substituer:
    - $P(S0)$ est vraie $\rightarrow$ $P(SS0)$ est vraie
  - Et pour $n = SS0$ je peux substituer:
    - $P(SS0)$ est vraie $\rightarrow$ $P(SSS0)$ est vraie
  - ... On peut dérouler une infinité de propriétés qu'on énonce vraie, une pour chaque entier

---

# Exemple

- Montrons que $0 + n = n + 0$
  - Parait évident, mais il faut que ça fonctionne « syntaxiquement »
  - Notre définition de l’addition ne permet que de calculer directement la partie gauche du $=$
    - C'est la règle 1. $0 + x \rightarrow x$
    - Mais la partie droite n'est pas de la forme de la règle 2. $Sn + x \rightarrow S(n + x)$
  - On doit donc raisonner par récurrence
- On pose la propriété $P(n)$: $0 + n = n + 0$
- On traduit $P(0)$: $0 + 0 = 0 + 0$
  - C’est bien vrai
- On doit montrer $P(n) => P(Sn)$
  - On suppose que $P(n)$ est vrai, donc que $0 + n = n + 0$ pour un certain $n$
  - On étudie $P(Sn)$: $0 + Sn = Sn + 0$
    - on doit montrer que cette égalité est vraie en ayant supposé $0 + n = n + 0$

---

# Exemple

- $0 + Sn = Sn + 0$ ?
  - On doit montrer que la partie gauche est égale à la partie droite
  - On va calculer les deux indépendament et voir si on obtient la même chose
    - On oublie pas qu'on a supposé $0 + n = n + 0$
- $0 + Sn \rightarrow Sn$ par application de la règle 1. $0 + x \rightarrow x$
- $Sn + 0 \rightarrow S(n + 0)$ par application de la règle 2. $Sn + x \rightarrow S(n + x)$
  - Or on a supposé $0 + n = n + 0$
  - Donc $Sn + 0 \rightarrow S(n + 0) \rightarrow S(0 + n)$
  - Or $S(0 + n) \rightarrow Sn$ par application de la règle 1. $0 + x \rightarrow x$
  - Donc $Sn + 0 \rightarrow Sn$
- On a bien $0 + Sn \rightarrow Sn$ et $Sn + 0 \rightarrow Sn$ donc $0 + Sn = Sn + 0$
- On a montré qu'en supposant $P(n)$ ($0 + n = n + 0$) vraie, on a forcement $P(Sn)$ ($0 + Sn = Sn + 0$) vraie
  - Et puisque $P(0)$ ($0 + 0 = 0 + 0$) est vrai, alors $P(n)$ est vraie pour tout entier $n$

---

# Exercice: démontrer par récurrence la distributivité ?

- Soit $a$ et $b$ des entiers fixé, démontrer par récurrence que $n \times (a + b) = n \times a + n \times b$

---

# Substitution et égalité

- Dans les slides précédentes j'ai utilisé le symbole $=$ de manière assez informelle
- Ecrire $A = B$ est vraie, cela signifie que l'expression à gauche est sémantiquement toujours égale à l'expression à droite
- Si on est capable de construire une suite de substitution $A \rightarrow ... \rightarrow B$ et/ou $B \rightarrow ... \rightarrow A$
  - Ou encore $A \rightarrow ...C$ et $B \rightarrow ...C$
- Alors on conclue $A = B$ est vraie, cela nous permet de passer de la syntaxe à la sémantique
- Le passage de la sémantique a la syntaxe n'est par contre pas garanti comme on le verra plus tard
  - On peut avoir $A = B$ sans être capable de le démontrer mécaniquement, par enchainement de substitutions

---

# Arithmétique de Peano

- Ce qu’on a vu correspond aux axiomes de Peano:
  - L'élément appelé zéro et noté $0$ est un entier naturel.
  - Tout entier naturel $n$ a un unique successeur, noté $Sn$ qui est un entier naturel.
  - Aucun entier naturel n'a $0$ pour successeur.
  - Deux entiers naturels ayant le même successeur sont égaux.
  - Si un ensemble d'entiers naturels contient $0$ et contient le successeur de chacun de ses éléments, alors cet ensemble correspond aux entiers naturels
- Une grande partie des maths modernes peuvent être construite par-dessus ces axiomes

---
layout: intro
class: text-center
---

# La notation en base

---

# Récapitulatif

- On a vu une formalisation des nombres entier, notés $0$, $S0$, $SS0$, ...
- On a vu une définition de l'addition et de la multiplication avec cette formalisation
- On a vu qu'on peut démontrer des choses avec cette formalisation

---

# Représentation en base 10

- Mais peu pratique: les S ça prend de la place
- L’approche par substitution c’est long
- Et si on faisait plutôt des paquets de 10 ?
  - Parce qu’on a dix doigts
- On va construire un algo de substitution pour transformer la notation 0, S0, SS0, SSS0, … vers la notation habituelle 0, 1, 2, …

---

# Passage en base 10

- Si le nombre de S est inferieur à 10, on remplace par le chiffre correspondant
  - $0 \rightarrow 0$
  - $S0 \rightarrow 1$
  - $SS0 \rightarrow 2$
  - ...
  - $SSSSSSSSS0 \rightarrow 9$
- Sinon on décompose en la somme d’un produit par SSSSSSSSSS0 (= 10) et d’un nombre remplaçable par un chiffre
- On recommence sur le facteur de SSSSSSSSSS0

---

# Exemple

- $SSSSSSSSSSSSSSSSSSSSSSS0$
- $= SSSSSSSSSS0 + SSSSSSSSSS0 + SSS0$
- $= SSSSSSSSSS0 \times SS0 + SSS0$
- $= 23$

---

# Exponentiation

- L’opération de groupement récursif des S correspond à l’exponentiation, l’itération de la multiplication
- Soit $x$, $n$ des nombres entier naturels, on pose:
  - $x^0 \rightarrow 1$
  - $x^{Sn} \rightarrow x^n \times n$
- Propriété:
  - $x^{a + b} = x^a \times x^b$

---

# Avec l’exponentiation

- $115 = 100 + 10 + 5 = 10^2 \times 1 + 10^1 \times 1 + 10^0 \times 5$
  - $= SSSSSSSSSS0^{𝑆𝑆0} \times S0 + SSSSSSSSSS0^{𝑆0} \times S0 + SSSSSSSSSS0^0 \times SSSSS0$
- De manière générale, un nombre écrit $a_ka_{k - 1}...a_0$ en base 10 a pour valeur:
  - $10^ka_k + 10^{k-1}a_{k - 1} + ... + 10^0a_0$
- Et peut être convertis en notation $S$ par substitution:
  - $subs(a_ka_{k - 1}...a_0) = SSSSSSSSSS0^{subs(k)} subs(a_k) + SSSSSSSSSS0^{subs(k - 1)} subs(a_{k - 1}) + ... + SSSSSSSSSS0^0 subs(a_0)$

---

# Autres bases

- On a choisit de faire des puissances de 10
- Avec puissances de 2 on obtient la notation binaire
  - On a deux symboles de chiffre, 0 et 1
- Avec puissance de 16 on obtient la notation hexadécimale
  - On a seize symboles de chiffre, 0, 1, ..., 9, A, B, ..., F
- La notation n’est qu’un autre nom pour un nombre, le concept sous jacent reste celui d’une quantité d’objets

---

# Avantages des bases

- Taille de la notation beaucoup plus petite
  - Par exemple, le nombre 123456789 est très grand, mais sa notation en base 10 ne contient que 9 chiffres
  - Le nombre de symbole à utiliser pour représenter un nombre $n$ en base $k$ est de l’ordre de $\log_k(n)$
- Algorithmes efficaces pour addition, multiplication, soustraction, division
  - Car la taille de la notation est petite par rapport aux nombres

---

# Algorithme de l’addition

- Celui qu’on voit en primaire
- On démontre qu’il fonctionne grâce à la décomposition en puissance

---

# Exemple

- $123 + 78$
  - $123 = 10^2 \times 1 + 10^1 \times 2 + 10^0 \times 3$
  - $78 = 10^1 \times 7 + 10^0 \times 8$
- $123 + 78 = 10^2 \times 1 + 10^1 \times 2 + 10^0 \times 3 + 10^1 \times 7 + 10^0 \times 8$
  - $= 10^2 \times 1 + 10^1 \times (2 + 7) + 10^0 \times (3 + 8)$
  - $= 10^2 \times 1 + 10^1 \times (2 + 7) + 10^0 \times (10 + 1)$
  - $= 10^2 \times 1 + 10^1 \times (2 + 7) + 10^1 + 10^0 \times 1$
  - $= 10^2 \times 1 + 10^1 \times (2 + 7 + 1) + 10^0 \times 1$
  - $= 10^2 \times 1 + 10^1 \times (2 + 7 + 1) + 10^0 \times 1$
  - $= 10^2 \times 1 + 10^1 \times 10 + 10^0 \times 1$
  - $= 10^2 \times (1 + 1) + 10^0 \times 1$
  - $= 10^2 \times 2 + 10^1 \times 0 + 10^0 \times 1 = 201$

---

# Algorithme de la multiplication

- $123 \times 78 = 9594$
  - $= 123 \times (10^1 \times 7 + 10^0 \times 8)$
  - $= 123 \times 10^1 \times 7 + 123 \times 10^0 \times 8$
- Le premier terme a $10^1$ pour facteur, c’est ce qui vient rajouter un 0 sur la deuxième ligne d’addition dans l’algo de multiplication
- La puissance qui augmente, c’est la retenue

---
layout: intro
class: text-center
---

# Créer des nombres

---

# Je pense à un nombre

- Je pense à un nombre, je le multiplie par 3, j’ajoute 2, j’obtiens 11, quel est ce nombre ?
- Traduit l’équation $3n + 2 = 11$
- La solution est $n \rightarrow 3$
  - $3n + 2 = 11 \rightarrow 3 \times 3 + 2 = 11 \rightarrow 9 + 2 = 11 \rightarrow 11 = 11$
- Résoudre une équation c'est trouver une substitution des variables qui résulte sur une égalité vraie

---

# Résoudre une équation

- On résout une équation en appliquant la même opération de chaque coté du égal
  - C’est à nouveau de la substitution, à $A = B$ on peut substituer $op(A) = op(B)$
  - $A = B \rightarrow op(A) = op(B)$
- On cherche à isoler l’inconnue en inversant toutes les opérations qui s’appliquent dessus par ordre inverse de priorité
  - $3n + 2 = 11$
  - $\rightarrow 3n + 2 – 2 = 11 – 2$
    - ici $op(A) = A - 2$
  - $\rightarrow 3n + 0 = 9$
  - $\rightarrow 3n = 9$
  - $\rightarrow \frac{3n}{3} = \frac{9}{3}$
    - ici $op(A) = \frac{A}{3}$
  - $\rightarrow n = 3$
- Mais on a n’a pas définit $a – b$ et $\frac{a}{b}$ !

---

# Les opérations inverses

- L’addition s’inverse par soustraction
  - Si $n$ est tel que $n = a + b$, alors on autorise la substitution $n – a \rightarrow b$
    - La soustraction se définit à partir de l’addition
    - Par exemple on a $5 = 3 + 2$, on a donc $5 - 3 \rightarrow 2$
  - En théorie à ce stade on ne peut pas soustraire si $a > n$
    - $b = 3 – 5 \rightarrow 3 = 5 + ?$ (la solution entière n’existe pas)
- La multiplication s’inverse par division
  - Si $n$ est tel que $n = a \times b$, alors on autorise la substitution $b = \frac{n}{a}$
    - La division se définit à partir de la multiplication
    - Par exemple on a $6 = 3 \times 2$, on a donc $\frac{6}{3} \rightarrow 2$
  - En théorie à ce stade on ne peut pas diviser si n ne s’écrit pas comme un produit contenant a
    - $b = \frac{12}{5} \rightarrow 12 = 5 \times ?$ (la solution entière n’existe pas)

---

# Equation à solution « négative »

- Prenons l’équation $n + 5 = 0$
- Pas de solution a priori, la représentation en quantités de 🍎 ne traduit pas ce genre de concept
- Représentations intuitives possibles
  - La notion de dette:
    - $n + 🍎🍎🍎🍎🍎 = 0$ ?
    - On me donne 5 pommes, mais mon total est zéro. C'est probablement que j’en dois 5 à quelqu’un. $n$ est donc ce nombre qui représente ma dette de 5 pommes.
  - La notion de distance, si j’avance de 5 j’atteins 0. $n$ est donc cette position qui me permet d’atteindre 0 en avançant de 5.

---

# Création des nombres négatifs

- On « étend » les nombres entiers en « créant » l’ensemble des solutions aux équation de la forme $n + a = 0$
  - Nombre entier naturel + nombres négatifs = nombre entiers relatifs, ou juste nombres entiers
- Si $n + a = 0$, on pose la notation $n \rightarrow -a$
  - Par exemple, si $n + 5 = 0$, alors $n \rightarrow -5$, on peut donc écrire $-5 + 5 = 0$
- En définissant cette notation, on s’autorise une nouvelle règle de substitution:
  - $n + -n \rightarrow 0$ quelque soit $n$

---

# Création d’objets

- De manière générale, les mathématiciens créé des entités (nombres ou autres) qui respectent certaines propriétés
- Lorsqu’on pose des équations qui n’ont pas de solution, on peut se permettre d’étendre notre univers avec de nouvelles entités qui solutionnent ces équations
- A condition que ces entités se comportent de manière cohérente par rapport au cadre initial (même propriétés sur les opérations, pas d’incohérences)

---

# Notation et sens

- On a choisit le symbole « - » pour représenter les nombres négatifs, on aurait pu prendre ce qu’on veut
- Il est essentiel que les propriétés de l’addition (et de la soustraction) restent les même lorsque appliqués au nombre négatifs
- Syntaxiquement, le $–$ unaire n’est pas la même chose à priori que l’opération binaire $–$ entre deux nombres
  - Mais on pourrait démontrer que la sémantique des deux symboles est proche, ce qui justifie d'utiliser le même symbole
  - Par exemple, on pourrait vérifier des propriétés comme:
    - $0 - n = -n$ pour tout $n$
    - $(-1) \times n = -n$ pour tout $n$
  - Cela mène à des règles de calcul apprisent au collège comme $a + -b = a – b$, ou $a - -b = a + b$
    - Ces règles à priori arbitraire se démontrent
- Lorsque des concepts se rejoignent (ici "soustraction" et "nombre négatif"), les mathématiciens choisissent des notations communes pour traduire ce lien (ici le symbole $-$)

---

# Equation à solution « rationnelle »

- Prenons l’équation $n \times 5 = 3$
- Pas de solution a priori, la représentation en quantités de 🍎 ne traduit pas ce genre de concept
- Représentations intuitives possibles:
  - Découpe d’un gâteau en parts: le nombre $n$ dans $n \times 5 = 3$ est un nombre représentant 3 parts sur 5, on le note $\frac{3}{5}$
  - Découpage multi-résolution de la droite des entiers, pratique pour une représentation géométrique des opérations

---

# Création des nombre rationnels

- On « étend » les nombres entiers en « créant » l’ensemble des solutions aux équation de la forme $n \times b = a$
  - Nombre entier + nombres fractionnaires = nombre rationnels
- Si $n \times b = a$, on pose la notation $n \rightarrow \frac{a}{b}$
- Comme pour les négatifs, sa notation et la relation à l’addition/soustraction, on pourrait refaire un certain nombre de démonstration formelles pour vérifier que cette notation conduit à des propriétés respectant les règles usuelles de la multiplication/division.
  - Exemple: on pourrait tenter de montrer que la notation formelle $\frac{a \times b}{c}$ est conceptuellement équivalente au nombre résultant de l’opération $a \times \frac{b}{c}$, que $\frac{a}{a}$ correspond au nombre 1, etc.

---

# Représentation géométrique

<div class="flex justify-center">
  <img border="rounded" src="/rationnels.png" width="600"/>
</div>

---

# Les nombres rationnels sont t’il suffisants ?

- Peut-on représenter n’importe quel longueur géométrique avec un rationnel ?
- A priori oui
  - Soit $x$, $y$ deux rationnels, il existe une infinité de rationnels dans l’intervalle $[x, y]$
  - Le milieu de l’intervalle est le rationnel $\frac{x + y}{2}$
  - On peut découper autant qu’on veut

---

# Le nombre $\sqrt{2}$

- Le nombre $\sqrt{2}$ peut être construit géométriquement
- (montrer figure)

---

# L’équation de solution $\sqrt{2}$

- $\sqrt{2}$ est la solution de l’équation $n^2 = 2$
- Ce nombre est t’il rationnel ?

---

# Démonstration

- Supposons qu’il existe $a, b$ entiers tel que $\sqrt{2} = \frac{a}{b}$  avec
  - $a$ et $b$ sans facteurs communs (sinon on simplifie la fraction)
    - Par exemple, si $a=21$ et $b=14$, alors $a=7\times3$ et $b=7\times2$
    - On aurait $\frac{a}{b} = \frac{21}{14} = \frac{7\times3}{7\times2} = \frac{3}{2}$
    - Plutot que s'intéresser à $a=21$ et $b=14$, on peut simplifier et s'intéresser directement à $a=3$ et $b=2$
  - Cela implique que $a$ et $b$ ne sont pas pair tous les deux
    - Sinon $2$ est un facteur commun
- $\sqrt{2} = \frac{a}{b} \iff 2 = \frac{a^2}{b^2}  \iff a^2 = 2b^2$
- Donc $a^2$ est pair ce qui implique $a$ pair. On peut donc trouver $k$ tel que $a = 2k$
- $a^2 = 2b^2 \iff 4k^2 = 2b^2 \iff 2k^2 = b^2$
- Donc $b^2$ est pair ce qui implique $b$ pair. Contradiction avec "$a$ et $b$ ne sont pas pair tous les deux", donc $\sqrt{2}$ ne peut s’écrire comme fraction de 2 nombres entiers

---

# Création des nombres réels

- Un ensemble nettement plus compliqué à définir formellement que ce qu’on a vu jusqu’à présent
- Géométriquement, l’ensemble des longueurs de segment, des aires, …
- Numériquement, plusieurs définitions avancées possibles
  - Coupures de Dedekind, un réel = l’ensemble des rationnels qui lui sont strictement inferieurs
  - Les suites de Cauchy, un réel = une suite de rationnels convergeant vers lui
  - Approche axiomatique, série de définitions caractérisant l’ensemble en question
  - https://www.wikiwand.com/fr/Construction_des_nombres_r%C3%A9els

---
layout: intro
class: text-center
---

# Représentation informatique

---

# Représentation binaire

- Les nombres sont représenté en base 2 au niveau machine
- En électronique numérique on travaille directement avec des composants implémentant un calcul binaire
- Les processeurs implémentent matériellement les opérations classiques sur les int et les float de tailles 8, 16, 32, 64, 128, 256

---

# Nombres entiers

- Le type int décliné sous ses formes int8 (char, 8 bits, un octet), int16 (short, 16 bits, un mot), int32 (int, 32 bits, 4 octets, deux mots), int64 (long long int, 64 bits, 8 octets, 4 mots)
- En version non signée: unsigned int
  - Peut représenter les nombres de $0$ à $2^n - 1$ ou n est le nombre de bits
  - On représente un nombre par sa notation en base 2
    - $14786528 \rightarrow 00000000111000011001111111100000$
- En version signée:
  - On utilise un bit pour le signe

---

# Positifs et négatifs

- Plusieurs manières possibles de représenter des positifs et négatifs
  - Signe + Magnitude
  - Complément à un
  - Complément à deux
    - La méthode utilisée sur les CPU modernes

---

# Signe + Magnitude

- Méthode la plus naive
- Un bit pour le signe (0 = positif, 1 = negatif)
- Le reste on écrit le nombre en valeur absolue en base 2
  - $58 = 00111010$
  - $-58 = 10111010$
- On peut représenter les nombre de $-2^{n - 1} -1$ à $2^{n - 1} -1$
- Problèmes:
  - 2 représentations pour zéro
    - $0 = 00000000 = 10000000$
  - Arithmétique compliquée

---

# Complément à un

- On inverse tous les bits de la représentation binaire du positif
  - $58 = 00111010$
  - $-58 = 11000101$
- On peut représenter les nombre de $-2^{n - 1}-1$ à $2^{n - 1}-1$
- L’arithmétique est simple
  - On fait une addition « classique » avec retenue
  - S’il y a une retenue à la fin on la rajoute à droite
- Problèmes:
  - 2 représentations pour zéro
    - $0 = 00000000 = 11111111$

---

# Complément à deux

- On inverse tous les bits de la représentation binaire du positif et on ajoute un
  - $58 = 00111010$
  - $-58 = 11000101 + 1 = 11000110$
- On peut représenter les nombre de $- 2^{n - 1}$  à $2^{n - 1}-1$
- Une seule représentation pour zéro
  - En effet, si on essaye de faire $-0 = - 00000000 = 11111111 + 1 = 00000000$
- Arithmétique ultra simple
  - Addition « classique » avec retenue
  - Si retenue à la fin, on l’ignore
  - Soustraction = ajout du négatif

---

# Complément à deux sur 32 bits

- On doit complémenter tous les bits
  - $58 = 00000000000000000000000000111010$
  - $-58 = 11111111111111111111111111000110$
- En code, on a `–n == ~n + 1`

---

# Overflow/underflow

- La représentation finie + arithmétique implique du danger:
  - $2^{31}-1 = 2147483647 = 01111111111111111111111111111111$
  - $2147483647 + 1 = 10000000000000000000000000000000$
    - $= - 2^{31} = -2147483648$

---

# Trick

- On peut obtenir `MAX_UINT` en faisant `(unsigned int)-1`
  - En effet en int $-1 = 11111111111111111111111111111111$
  - Mais c’est aussi $2^{32}-1$ en unsigned int
  - Le cast des int vers uint ne change pas la représentation (c’est gratuit)

---

# Remarque en base 10

- Notez qu’en base 10 on pourrait aussi représenter les négatifs en complément à 10
  - On fait le complément à 9 de chaque chiffre et on ajoute 1
  - C’est comme avoir une infinité de 9 à gauche sur les négatifs
  - Comme on a une infinité virtuelle de 0 à gauche sur les positifs
- $-58 \rightarrow ...941 + 1 \rightarrow ...942$
- Essayons $58 + -58$
  - $...058 + ...942 = ...000$
- $-1 \rightarrow ...98 + 1 = ...9$
- Cela donne une belle symétrie
  - $...81 (-19)$, $...82 (-18)$, ..., $...89 (-11)$, $...90 (-10)$, $...91 (-9)$, ..., $...98 (-2)$ $...99 (-1)$, $...0$, $...01$, $...02$
  - Cela permet d’étendre la notation en base 10 sans introduire de symbole supplémentaire

---

# Little endian / Big endian

- On est habitué à se représenter les nombres de gauche à droite:
  - 58 = 00111010
  - On s’attendrait a avoir: 00000000 00000000 00000000 00111010 sur 32 bits
- Cela dépend du processeur
  - Little endian = 00111010 00000000 00000000 00000000
  - Les octets sont inversé par rapport à notre représentation classique
- Mnémotechnique: Little = petit bouts d’abord

---

# Code

- Voir le fichier [integers.cpp](/integers.cpp)

---

# Nombre flottants

- On pourrait représenter les nombres décimaux simplement
  - Un int pour la partie entière
  - Un uint pour la partie décimale
  - Une représentation en point fixe => un nombre de chiffres après la virgule, et on peut tout représenter en int
- Problème: même résolution pour toutes les tailles de nombre
- Or on manipule plus souvent des petits nombres
  - => besoin de plus de précision proche de zéro

---

# Norme IEEE-754

- Sur 32 bits:`seeeeeeeemmmmmmmmmmmmmmmmmmmmmmm`
  - `s`:le bit de signe
  - `e`:un exposant biaisé, encodé en uint8
  - `m`:une mantisse, encodé en uint23
- La valeur du nombre est $(-1)^s2^{e - bias}(1 + 0.m)$
  - Ou $0.m$ est le nombre dont la partie décimale écrit en binaire est $m$
  - Ou $bias$ est $2^{8−1}−1=127$
  - On utilise le nombre de bit de l’exposant pour calculer le biais

---

# Remarque sur puissance négative

- On a $x^{-n} = \frac{1}{x^n}$
- En effet: $1 = x^{0} = x^{n + -n} = x^nx^{-n} \iff x^{-n} = \frac{1}{x^n}$
- Donc $2^{-n} = \frac{1}{2^n}$ ce qui nous permet des facteurs de plus en plus précis dans dans $(-1)^{s}2^{e - bias}(1 + 0.m)$

---

# Notation décimale binaire

- Le nombre noté en binaire $0.m_1m_2...m_k$ à pour valeur:
  - $m_1 2^{-1} + m_2 2^{-2} + ... + m_k 2^{-k} = \frac{m_1}{2} + \frac{m_2}{2^2} + ... + \frac{m_k}{2^k}$

---

# Expérimentation sur 4 bits positif

- Sur la représentation `eemm`, le biais est $2^{2−1}−1=  1$
- Commençons par $1 + 0.mm$
  - $mm = 00$ => $1 + 0.00 = 1$
  - $mm = 01$ => $1 + 0.01 = 1 + 0.25 = 1.25$
  - $mm = 10$ => $1 + 0.10 = 1 + 0.5 = 1.5$
  - $mm = 11$ => $1 + 0.11 = 1 + 0.5 + 0.25 = 1.75$
- Et $2 ^{e - bias} = 2^{e - 1}$
  - $ee = 00$ (0), on a $2^{0−1}=0.5$ (0.5, 0.625, 0.75, 0.875)
  - $ee = 01$ (1), on a $2^{1−1}=1$ (1, 1.25, 1.5, 1.75)
  - $ee = 10$ (2), on a $2^{2−1}=2$ (2, 2.5, 3, 3.5)
  - $ee = 11$ (3), on a $2^{3−1}=4$ (4, 5, 6, 7)
- => On obtient assez peu de nombres, avec des trous
- Ou est 0 ?

---

# Rajout de cas particuliers

- si l'exposant biaisé et la mantisse sont tous deux nuls, le nombre est ±0 (selon le bit de signe)
- si l'exposant biaisé est égal à $2^8−1=255$, et si la mantisse est nulle, le nombre est ±infini (selon le bit de signe)
- si l'exposant biaisé est égal à $2^8−1=255$, mais que la mantisse n'est pas nulle, le nombre est NaN (not a number : pas un nombre)

---

# Représentation en Level of Detail

- Sur 32 bits: `seeeeeeeemmmmmmmmmmmmmmmmmmmmmmm`
- On a $2^{23}$ combinaison possible de mantisse, qui représente des nombres à virgule fixe de la forme $1 + m_1 2^{-1} + m_2 2^{-2} + ... + m_{23} 2^{-23}$
- `eeeeeeee` permet de scaler tous ces nombres de $2^{−126}$ à $2^{127}$
- Lorsque `eeeeeeee` augmente, l’écart entre toutes les combinaisons augmente également
- A partir de $2^{23}$ on a même plus de virgule
- A partir de $2^{24}$ on avance de 2 en 2

---

# Avantages et Limites

- Limites
  - Très peu de précision pour les grands nombres
  - Représentation ambigüe, cas particuliers
- Avantages
  - Très grande précision pour les petits nombres
  - Calcul scientifique à petite échelle
- Conclusion
  - Si besoin de manipuler des grand nombres, les floats ne sont pas adapté
  - Ou alors changer d’espace via scale

---

# Code

- Voir le fichier [floats.cpp](/floats.cpp)

---

# Document "Binary Fundamentals"

- Un pdf récapitulatif sur la représentation et les opérations binaire: [Binary Fundamentals](/binary_fund.pdf)

---
layout: intro
class: text-center
---

# TP: Algorithmique numérique

---

# Itératif, récursif

- Juste un point pour être sur que tout le monde est ok
- En gros itératif = algos avec des boucles
- récursif = algos avec des fonctions qui se rappelle
  - C’est ce qu’on a fait pour définir addition, multiplication, …
    - $n + 0 \rightarrow n$
    - $n + Sm \rightarrow S(n + m)$
    - `plus(n, 0) = n`
    - `plus(n, m+1) = plus(n, m)+1`

---

# Calcul de factorielle

- La fonction factorielle de $n$ notée $n!$ est définie par:
  - $0! \rightarrow 1$
  - $n! \rightarrow 1 \times 2 \times ...  \times n$ pour $n > 0$
- On remarque que $n! = n \times (n - 1)!$
- Ecrire la fonction `facto_ite(n)` qui calcule la factorielle en itératif
- Ecrire la fonction `facto_rec(n)` qui calcule la factorielle en récursif

---

# Suite de Fibonacci

- La suite de Fibonacci est définie par:
  - $F_0 \rightarrow 0$
  - $F_1 \rightarrow 1$
  - $F_n \rightarrow F_{n-1} + F_{n-2}$ pour $n > 1$
- Ecrire la fonction `fibo_rec(n)` qui calcule un élement de la suite en récursif
- Ecrire la fonction `fibo_ite(n)` qui calcule un élement de la suite en itératif
- Comparez les performances, comment expliquer une telle différence ?

---

# Calcul du nombre d’or et $\sqrt{5}$

- On peut utiliser des définitions de suites et leur limites pour calculer des nombres irrationnels
- Le nombre d’or est défini par:
  - $\phi = \lim_{n \rightarrow \infty} \frac{F_{n+1}}{F_n}$
  - L'opérateur limite $\lim_{n \rightarrow \infty}$ indique que plus $n$ augmente, plus $\frac{F_{n+1}}{F_n}$ s'approche du nombre d'or
- Ecrire une fonction `golden_phi(n)` qui calcule une approximation du nombre d’or (plus n est élevé, plus l’approximation doit être précise)
- On a également:
  - $\phi = \frac{1 + \sqrt{5}}{2}$
- Ecrire une fonction `sqrt5(n)` qui calcule une approximation de $\sqrt{5}$. Comment vérifier la qualité de l’approximation ?

---

# Elévation à la puissance

- Trouver un algorithme efficace pour implémenter une fonction `my_pow(a, n)` (avec a flottant, n entier) calculant $a^n$

---
layout: intro
class: text-center
---

# Projet 1 – Arithmatoy

---

# Sujet

- L'objectif de ce projet est d'implémenter en C les algorithmes d'addition, soustraction et multiplication vu à l'école primaire.
- Vous trouverez le sujet et les instructions dans le [README du projet](https://gitlab.com/maths-[SUPPRIME_2600]/monorepo/-/blob/main/apps/arithmatoy/README.md?ref_type=heads).
