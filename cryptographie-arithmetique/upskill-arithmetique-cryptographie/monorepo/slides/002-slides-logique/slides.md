---
theme: seriph
layout: cover
highlighter: shiki
drawings:
  persist: false
background: /alex-padurariu-VxtWBOQjGdI-unsplash.jpg
---

# Maths [SUPPRIME_2600]

Logique

---
layout: intro
class: text-center
---

# Récapitulatif

---

# Ce qu'on a vu

- Fondations mathématiques de l'arithmétique
  - Définition du concept de nombre
  - Maths "bas niveau"
  - Constructions syntaxiques simples
  - Règles simples et algorithmiques
  - Distinction syntaxe / sémantique sur les nombres
    - Notation successeur vs notation base 10
- On a vu quelques notions de logique
  - Démonstration
  - Vérité
- On a fait un peu de code manipulant des maths sur les nombres

---

# Fondations de l'arithmétique

- Axiomes de Peano
  - L'élément appelé zéro et noté $0$ est un entier naturel.
  - Tout entier naturel $n$ a un unique successeur, noté $Sn$ qui est un entier naturel.
  - Aucun entier naturel n'a $0$ pour successeur.
  - Deux entiers naturels ayant le même successeur sont égaux.
  - Si un ensemble d'entiers naturels contient $0$ et contient le successeur de chacun de ses éléments, alors cet ensemble correspond aux entiers naturels
- Mais qu'est ce qu'un axiome ?
  - Proposition que l'on affirme vraie
  - Mais qu'est ce qu'une proposition ?
  - Qu'est ce que "vrai" ?
  - On a besoin d'une formalisation de la logique (une syntaxe, une sémantique, des règles mécaniques)

---

# Programme de la semaine

- Logique
- Calculabilité
- Algorithmique, complexité, formalisation des problèmes
- Session pratique et présentation du projet

---
layout: intro
class: text-center
---

# Introduction

---

# Formaliser la logique

- Notion de vérité ?
  - Le vrai, le faux
- Enoncé mathématiques logiques
  - Enoncés de base
  - Combinaison d'énoncés (conjonction, disjonction, négation, implication, équivalence)
- Construire des démonstrations
  - En logique, on veut manipuler les démonstrations elle même (méta-mathématique)
  - On veut donc formaliser (mécaniser) la notion même de démonstration
- A la frontière entre mathématique et philosophie
  - Des applications concrètes en informatique et électronique

---

# Syntaxe et sémantique

- Syntaxe
  - Donne les symboles et les règles que l'on peut utiliser pour combiner ces symboles
- Sémantique
  - Donne du sens aux symboles et constructions syntaxiques
  - Par example, dire que la proposition "L'élément appelé zéro et noté $0$ est un entier naturel." est vraie, c'est de la sémantique
    - On a besoin d'une syntaxe pour exprimer cette sémantique dans un langage logique commun à toutes les mathématiques
- Une question fondamentale des maths:
  - Est ce que la vérité d'un théorème peut toujours être établi par déduction mécanique ?
  - Autrement dit, est ce que la sémantique est conséquence syntaxique ?

---
layout: intro
class: text-center
---

# Logique propositionnelle

---

# Les propositions

- Une proposition est une construction syntaxique (formule) censée parler de vérité.
  - En arithmétique on opère sur des nombres, avec des opérateurs d'addition, multiplication, ...
  - En logique propositionnelle, on opère sur des valeurs de vérité `vrai` ou `faux`, avec des opérateurs logiques (`et`, `ou`, `non`, `implique`, ...)
- Le calcul des propositions définit les règles qui relient les propositions entre elles sans en examiner le contenu.

---

# Définition syntaxique

- Définition syntaxique des propositions
  - On se donne une infinité de variables propositionnelles $A_1, A_2, ...$ qui sont des propositions
  - Les deux constantes $0$ et $1$ sont des propositions ($0$ représente `faux` et $1$ représente `vrai`)
  - Si $A$ et $B$ sont des propositions alors:
    - $(\neg A)$ est une proposition et représente `non` $A$, la négation
    - $(A \land B)$ est une proposition et représente $A$ `et` $B$, la conjonction
    - $(A \lor B)$ est une proposition et représente $A$ `ou` $B$, la disjonction
    - $(A \Rightarrow B)$ est une proposition et représente $A$ `implique` $B$, l'implication
- On peut se passer des parenthèse en introduisant des règles de priorité

---

# Exemples de propositions

- $\neg(A_1 \land A_2) \Rightarrow A_3$
- $A_1 \Rightarrow (A_2 \lor (A_3 \Rightarrow A_4) \Rightarrow \neg A_5$)
- $0 \land 1 \Rightarrow A_1$
- Pour donner un sens à ces formules, il faut définir les règles de calcul propositionnel

---

# Calcul propositionnel

| $A$ | $B$ | $\neg A$ | $A \land B$ | $A \lor B$ | $A \Rightarrow B$ |
|-----|-----|----------|-------------|------------|--------------- |
| 0   | 0   | 1        | 0           | 0          | 1              |
| 0   | 1   | 1        | 0           | 1          | 1              |
| 1   | 0   | 0        | 0           | 1          | 0              |
| 1   | 1   | 0        | 1           | 1          | 1              |

- L'univers de la logique propositionnelle est très réduit
  - Seulement 2 valeurs de vérité
  - Il n'existe que $2^4 = 16$ opérateurs binaires possibles.
- Les tables de calcul donne un sens aux opérateurs
  - On passe de la syntaxe à la sémantique
  - On parle de calcul sémantique

---

# Table complète des opérateurs binaires

| $A$ | $B$ |F|$\land$| | | | |$\oplus$|$\lor$|$\downarrow$|$\Leftrightarrow$| || |$\Rightarrow$|$\uparrow$|V|
|-----|-----|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
| 0   | 0   |0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|1|
| 0   | 1   |0|0|0|0|1|1|1|1|0|0|0|0|1|1|1|1|
| 1   | 0   |0|0|1|1|0|0|1|1|0|0|1|1|0|0|1|1|
| 1   | 1   |0|1|0|1|0|1|0|1|0|1|0|1|0|1|0|1|

---

# Relations entre opérateurs

- On observe des relations entre opérateurs
- Lois de De Morgan (distributivité):
  - $\neg (A \land B)$ est équivalent à $\neg A \lor \neg B$
  - $\neg (A \lor B)$ est équivalent à $\neg A \land \neg B$

|$A$|$B$|$\neg A$|$\neg B$|$A \land B$|$\neg (A \land B)$|$\neg A \lor \neg B$|$A \lor B$|$\neg (A \lor B)$|$\neg A \land \neg B$|
|-|-|-|-|-|-|-|-|-|-|
|0|0|1|1|0|1|1|0|1|1|
|0|1|1|0|0|1|1|1|0|0|
|1|0|0|1|0|1|1|1|0|0|
|1|1|0|0|1|0|0|1|0|0|

---

# Syntaxe réduite

- Combien d'opérateurs au minimum sont nécessaire ?
  - $A \land B$ est équivalent à $\neg (\neg A \lor \neg B)$ (car $\neg (A \land B)$ est équivalent à $\neg A \lor \neg B$)
  - On peut définir le `et` à partir du `non` et du `ou` (et inversement)
  - $A \Rightarrow B$ est équivalent à $\neg A \lor B$
  - Donc on peut définir tous notre syntaxe primaire sur les opérateurs avec les seuls opérateurs $\neg$ et $\lor$

|$A$|$B$|$\neg A$|$A \Rightarrow B$|$\neg A \lor B$|
|-|-|-|-|-|
|0|0|1|1|1|
|0|1|1|1|1|
|1|0|0|0|0|
|1|1|0|1|1|

---

# Syntaxe minimale

- En fait on peut même montrer que le `non-ou` $\downarrow$ est suffisant pour définir tous les autres, de même que le `non-et` $\uparrow$
  - On dit que ces opérateurs sont universels
  - Pratique pour la création de circuits éléctroniques, un seul type de porte est nécessaire
- Pour ça on montre par table que le `ou` et le `non` peuvent s'exprimer avec ces opérateurs:

|$A$|$B$|$\neg A$|$A \lor B$|$A \downarrow B$|$A \downarrow A$|$(A \downarrow B) \downarrow (A \downarrow B)$|$A \uparrow B$|$A \uparrow A$|$(A \uparrow A) \uparrow (B \uparrow B)$|
|-|-|-|-|-|-|-|-|-|-|
|0|0|1|0|1|1|0|1|1|0|
|0|1|1|1|0|1|1|1|1|1|
|1|0|0|1|0|0|1|1|0|1|
|1|1|0|1|0|0|1|0|0|1|

---

# Praticité

- Exprimer toutes les formules avec un seul opérateur ce n'est pas très pratique en maths classiques
  - On y comprend rien
- En pratique dans les démonstrations on utilise le `et`, le `ou`, le `non`, le `implique` (`si ... alors ...`) et le `si et seulement si`
  - le `si et seulement si` a comme opérateur $A \Leftrightarrow B$, qui est équivalent à $(A \Rightarrow B) \land (B \Rightarrow A)$
- Cela reste pratique pour:
  - l'electronique
  - les programmes de logique formelle
  - les meta-mathématiques sur la syntaxe de la logique elle même (preuves par induction sur la structure des formules)

---

# Tautologies

- Une tautologie est une formule vraie quelque soit la valeurs des variables de cette formule
- Exemples:
  - $A \iff A$
  - $(A \iff B) \iff ((A \Rightarrow B) \land (B \Rightarrow A))$
  - $A \lor \neg A$ (tiers exclu)
  - $\neg A \iff (A \Rightarrow 0)$
  - $(A \Rightarrow B) \iff (\neg B \Rightarrow \neg A)$ (contraposée)
- On peut vérifier une tautologie en calculant son tableau de vérité. Par exemple:

| $A$ | $\neg A$ | $A \iff A$ | $A \lor \neg A$ | $A \Rightarrow 0$ | $\neg A \iff (A \Rightarrow 0)$ |
|-----|----------|------------|-----------------|----------------|------------------------------|
| 0   | 1        | 1          | 1               | 1              | 1                            |
| 1   | 0        | 1          | 1               | 0              | 1                            |

---

# Le sens des variables

- En calcul propositionnel, on ne s'interesse pas directement au sens des variables propositionnelles
- Le seul pré-requis est qu'une variable propositionnelle prenne une valeur de vérité
  - Par exemple une variable propositionnelle $A$ pourrait être `il fait beau`. Si il fait beau alors $A \Leftrightarrow 1$ est vrai, sinon $A \Leftrightarrow 0$ est vrai.
    - La valeur dépend d'un contexte
    - Ce contexte est en quelque sorte le cadre de raisonnement choisit: les axiomes
  - En maths des propositions de bases peuvent être des énoncés sur les nombres, par exemple:
    - `2 est pair`, qui est vrai dans le cadre de l'arithmétique
    - `5 = 6`, qui est faux dans le cadre de l'arithmétique
    - `x est supérieur à 8`, qui est une proposition à valeur de vérité variable en fonction de `x`

---
layout: intro
class: text-center
---

# Logique des prédicats

---

# Limites de la logique propositionnelle

- Le calcul propositionnel pose uniquement le minimum pour parler et calculer sur des valeurs de vérité
  - C'est donc un mode de calcul très primitif
  - On a besoin d'une logique plus puissante pour parler d'objets plus généraux comme les nombres directement dans les formules logiques
- Exemples de raisonnement qu'on ne peut pas formaliser en logique
  - Socrate est un homme
  - Les hommes sont mortels
  - donc Socrate est mortel
- Exemple en maths:
  - Le successeur d'un nombre pair est impair
  - 2 est un nombre pair
  - Le successeur de 2 est 3
  - donc 3 est impair

---

# Calcul des prédicats

- Le calcul des prédicats est construit par dessus le calcul des propositions
  - Aussi appelé logique du premier ordre
- Le calcul des prédicats utilise la syntaxe du calcul des propositions (constantes $0$ et $1$, variables propositionnelles, opérateurs) et rajoute des elements de plus haut niveau
- L'objectif est de donner plus de sens aux formules en fonction du contexte
- On rajoute:
  - le domaine et des variables pour représenter les elements de ce domaine
  - les prédicats
  - les quantificateurs
- On appelle formule une construction syntaxique avec ces elements

---

# Logique des prédicats: le domaine d'interpretation

- On se donne un domaine constitué d'élements sur lesquels on veut raisonner. Par exemple:
  - Le domaine des nombres
  - Le domaine des ensembles (au sens de la théorie des ensembles)
  - Le domaine des objets physiques
- En gros, un domaine = un univers d'exploration logique
  - En maths l'univers de base n'est pas les nombres, mais les ensembles

---

# Logique des prédicats: les prédicats

- Les prédicats sont des propositions qui dépendent d'une ou plusieurs variable $x, y, ...$ du domaine d'interpretation
- Un prédicat est donc vrai ou faux en fonction des valeurs qu'on lui donne, c'est une fonction logique
  - Sur le domaine des nombres entiers, on peut se donner les prédicats:
    - $pair(x)$ qui vaut 1 si $x$ est pair, $impair(x)$ qui vaut 1 si $x$ est impair
      - Avec des deux prédicat, on pourrait poser l'axiome: $pair(x) \Leftrightarrow \neg impair(x)$
    - $succ(x,y)$ qui vaut 1 si $y$ est le successeur de $x$ (On a alors $y = x + 1$ en arithmétique)
  - Sur le domaine des objets physiques
    - $h(x)$ vaut 1 si $x$ est humain
    - $m(x)$ vaut 1 si $x$ est mortel
- On peut construire de nouveaux prédicats en combinant des prédicats avec opérateurs et quantificateurs

---

# Logique des prédicats: quantificateurs

- Les quantificateurs $\forall$ et $\exists$
  - $\forall$ signifie "pour tout"
  - $\exists$ signifie "il existe"
- Exemple sur les nombres entiers:
  - $\forall x \exists y, succ(x,y)$: pour tout nombre entier x, il existe un nombre entier y qui est le successeur de x
  - $\forall x \forall y, pair(x) \land succ(x,y) \Rightarrow impair(y)$: pour tout x et pour tout y, si x est pair et y est successeur de x alors y est impair.
- Les quantificateurs permettent d'exprimer des valeurs de vérité aggregées sur les elements du domaines
  - Quelque soit le domaine (fini, infini, dénombrable ou pas)
- Les quantificateurs permettent de construire des formules closes (sans variables) à partir de prédicats qui contiennent des variables

---

# Rapport entre quantificateurs et opérateurs

- Le "pour tout" $\forall$ correspond à un `et` sur l'ensemble du domaine
  - $\forall x, p(x)$ traduit que la proposition $p(x)$ est vraie pour tous les elements du domaine
  - C'est comme écrire $p(x_1) \land p(x_2) \land ...$ ou $x_i$ énumère tous les elements du domaine
- Le "il existe" $\exists$ correspond à un `ou` sur l'ensemble du domaine
  - $\exists x, p(x)$ traduit que la proposition $p(x)$ est vraie pour au moins un element du domaine
  - C'est comme écrire $p(x_1) \lor p(x_2) \lor ...$ ou $x_i$ énumère tous les elements du domaine
- Les règles de De Morgan s'étendent aux quantificateurs:
  - $\neg (A \land B)$ est équivalent à $\neg A \lor \neg B$
  - $\neg (\forall x, p(x))$ est équivalent à $\exists x, \neg p(x)$
  - $\neg (A \lor B)$ est équivalent à $\neg A \land \neg B$
  - $\neg (\exists x, p(x))$ est équivalent à $\forall x, \neg p(x)$

---

# Formaliser un raisonnement naturel en logique des prédicats

- Socrate est un homme
  - Il faut un prédicat pour identifier socrate: $socrate(x)$ est vrai si $x$ est socrate
  - On peut alors poser l'axiome de l'existence de socrate: $\exists x, socrate(x)$
  - Il faut un prédicat qui indentifie les hommes: $homme(x)$ est vrai si $x$ est un homme
  - On peut alors poser l'axiome: $\forall x, socrate(x) \Rightarrow homme(x)$
- Les hommes sont mortels
  - Il faut un prédicat qui identifie les choses mortelles: $mortel(x)$ est vrai si $x$ est mortel
  - On peut alors poser l'axiome: $\forall x, homme(x) \Rightarrow mortel(x)$
- donc Socrate est mortel
  - $\forall x, socrate(x) \Rightarrow homme(x)$ est vrai (axiome)
  - $\forall x, homme(x) \Rightarrow mortel(x)$ est vrai (axiome)
  - Par substitution sur l'implication, on a $\forall x, socrate(x) \Rightarrow mortel(x)$

---

# Substitution sur l'implication ?

- C'est en fait une règle qu'on appelle le Modus-Ponens qui permet de passer de la logique propositionelle à la démonstration
- Si $A$ est vrai et $A \Rightarrow B$ est vrai, alors $B$ est vrai.
- On se permet donc de substituer $B$ à $A$ pour le reste du raisonnement.
- Le modus ponens est une règle de déduction
- Un système de déduction définit des règles de remplacement logique permettant de passer du calcul logique à la démonstration

---

# Formaliser un raisonnement mathématique en logique des prédicats

- Le successeur d'un nombre pair est impair
  - On pose l'axiome: $\forall x \forall y, succ(x,y) \land pair(x) \Rightarrow \neg pair(y)$
- 2 est un nombre pair
  - On pose l'axiome: $\forall x, deux(x) \Rightarrow pair(x)$
- Le successeur de 2 est 3
  - On pose l'axiome: $\forall x \forall y, deux(x) \land succ(x,y) \Rightarrow trois(y)$
- donc 3 est impair
  - On veut déduire $\forall y, trois(y) \Rightarrow \neg pair(y)$
  - Pour arriver à cette conclusion par substitution, il faut aller plus loin les système de déduction
  - Mais avant ça, a t-on vraiment besoin de poser un prédicat pour chaque nombre ? ou un prédicat pour exprimer la parité ?

---
layout: intro
class: text-center
---

# Théorie de la démonstration

---

# Théorie axiomatique

- Une théorie axiomatique est donnée par une série d'axiomes et leurs conséquences (qu'on appelle théorème)
  - "Les élements d'Euclide" est considéré comme la première théorie axiomatique et définit la géométrie euclidienne
  - La théorie axiomatique de Peano définit les nombres entiers naturels
  - La théorie des ensembles ZF définit les ensembles mathématiques
  - La théorie des groupes étudie les structures algébriques appelées groupes
- Axiomes: suite de formules closes qu'on affirme vraies
- On peut ensuite combiner ces formules en utilisant le calcul des prédicats
- On peut avoir une infinité d'axiomes, a condition qu'ils soient récursivement énumérable
  - C'est à dire qu'on peut les construire récursivement, par processus de substitution

---

# Axiomatique de Peano en logique des prédicats

- On a besoin des prédicats $zero(x)$, $succ(x, y)$, $egal(x, y)$
- L'élément appelé zéro et noté $0$ est un entier naturel.
  - $\exists x, zero(x)$
- Tout entier naturel $n$ a un unique successeur, noté $Sn$ qui est un entier naturel.
  - $\forall x \exists y, succ(x, y)$
- Aucun entier naturel n'a $0$ pour successeur.
  - $\forall x \forall y, zero(y) \Rightarrow \neg succ(x, y)$
- Deux entiers naturels ayant le même successeur sont égaux.
  - $\forall x \forall y \forall z, succ(x, z) \land succ(y, z) \Rightarrow egal(x, y)$
- Si un ensemble d'entiers naturels contient $0$ et contient le successeur de chacun de ses éléments, alors cet ensemble correspond aux entiers naturels
  - Pour toute formule $p(x)$ on pose l'axiome: $((\forall x, zero(x) \land p(x)) \land (\forall x \forall y, succ(x, y) \land (p(x) \Rightarrow p(y))) \Rightarrow \forall x, p(x)$

---

# Quelques remarques

- Pour définir l'addition et la multiplication il faudrait ajouter des axiomes
  - Ces axiomes nous permettrait ensuite d'appliquer des règles de déduction logique pour faire les substitution mécanique menant au calcul arithmétique
- On a utilisé un prédicat $egal(x, y)$ pour l'égalité
  - Les formalismes de plus haut niveau considère l'égalité comme une primitive du langage, avec son symbole $=$ comme relation binaire entre les elements du domaine
- On a utilisé un prédicat $zero(x)$ pour définir zéro
  - Ce prédicat agit comme un filtre sur tous les elements du domaine
  - Dans les langages du premier ordre, on s'autorise des construction syntaxique plus avancé à l'aide d'une signature logique
  - Une signature est une liste des symboles de constantes, de fonction ou de relation, chacun avec une arité (un nombre d'argument)
  - Une relation est un prédicat, une fonction un opérateur sur le domaine (par exemple $+$ et $\times$ sont des fonctions d'arité 2)

---

# Arithmétique de Peano en langage du premier ordre

- La signature est $\{0, s, +, \times \}$
- $\forall x, \neg (s(x) = 0)$
- $\forall x, (x = 0 \lor \exists y (x = s(y)))$
- $\forall x \forall y, (s(x) = s(y) \Rightarrow x = y)$
- $\forall x, x + 0 = x$
- $\forall x \forall y, (x + s(y) = s(x + y))$
- $\forall x, x \times 0 = 0$
- $\forall x \forall y, (x \times s(y) = x \times y + x)$
- Pour tout formule $p(x)$:
  - $(p(0) \land (\forall x, p(x) \Rightarrow p(s(x)))) \Rightarrow \forall x, p(x)$

---

# Formaliser le processus de démonstration

- Démontrer, c'est tenter de prouver qu'une formule est vraie
  - On peut le faire par table de vérité dans des cas simples, exemple: la tautologie $A \lor \neg A$, c'est du calcul
  - Dans le cas de formules utilisant des prédicats et quantificateurs c'est impossible
- Une preuve mathématique est souvent écrire dans un langage qui mélange le formel et l'informel
- C'est pratique et lisible, mais le mathématicien veut s'assurer qu'il est possible de formaliser tout ce processus
  - C'est à dire de formaliser un processus mécanique de substitution qui permet de passer des axiomes à la formule
- Pour cela on utilise un système de déduction
  - Une série de règles de substitution qui peuvent être utilisées pour transformer une formule en une autre
  - L'application d'un système de déduction est automatisable (en code)

---

# Systèmes de déductions

- Les systèmes principaux sont le Système à la Hilbert, la Déduction naturelle et le Calcul des séquents
- On a déjà vu le Modus-Ponens
  - Permet de passer d'une formule contenant une implication à une substitution (ou déduction)
  - Si $A$ est prouvé, et $A \Rightarrow B$ est prouvé, alors $B$ est prouvé
- On peut construire d'autres règles de déductions, par exemple:
  - Si $A$ est prouvé, alors $A \lor B$ est prouvé quelque soit B
  - Si $A$ et $B$ sont prouvé, alors $A \land B$ est prouvé
  - Le vrai est prouvé
  - Les axiomes qu'on a choisit sont prouvé
- Les règles cherchent à convertir une sémantique sur la vérité en un arbre de substitution mécanique
  - Elles permettent de prouver des formules logiques en construisant un arbre qui part des axiomes et qui applique des règles à chaque noeud
- Toutes les démonstrations mathématiques peuvent être formalisé par un arbre de déduction

---

# Règle de déduction: notation

- On se donne un système formel définit par des axiomes et un langage logique. Par exemple l'arithmétique formelle de Peano.
- On note $\vdash A$ lorsque la formule $A$ peut être dérivé des axiomes par déduction. En général $A$ est une formule qu'on cherche à prouver.
- On note $A_1, A_2, ..., A_n \vdash A$ lorsque la formule $A$ peut être prouvée par les formules $A_1, A_2, ..., A_n$
- Les règles de déduction permette de remonter d'une formule vers les axiomes
- On note $\frac{\Gamma_1 \vdash A_1 \quad ... \quad \Gamma_n \vdash A_n}{A_1, ..., A_n \vdash A}$ une règle de déduction
  - $\Gamma_i$ représente une séquence de formules qu'on suppose vraies
  - Si on peut remonter de $\Gamma_i$ vers les axiomes en appliquant d'autres règles, on construit un arbre de déduction
- Exemples:
  - La règle du modus-ponens s'écrit: $\frac{\Gamma \vdash A \quad \Gamma \vdash A \Rightarrow B}{\vdash B}$
  - La règle d'utilisation d'un axiome: $\frac{}{\Gamma, A \vdash A}$ lorsque $A$ est un axiome
  - Les règle d'élimination du `et`: $\frac{\Gamma \vdash A \land B}{\Gamma \vdash A}$ et $\frac{\Gamma \vdash A \land B}{\Gamma \vdash B}$

---

# Exemple en arithmétique de Peano

- Juste pour voir à quoi ressemble un arbre de déduction
  - Source: https://www.i2m.univ-amu.fr/perso/lionel.vaux/ens/imd-logique/
- On veut prouver "tout successeur d'un successeur est un successeur"
  - $\forall x (\exists y, x = SSy \Rightarrow \exists y, x = Sy)$

![](/arbre_deduction.png)

---

# Règle de déduction: combien de règles ?

- On peut construire autant de règle qu'on veut
- La seule contrainte: elles doivent préserver la sémantique de la logique, à savoir les valeurs de vérité
- On pourra chercher à avoir un minimum de règles quand on veut raisonner sur les démonstrations elles même (méta-mathématique)
- Et on voudra un maximum de règles pour construire des démonstration "lisible"
  - Un peut comme écrire des fonctions dans un programme pour factoriser des repetitions de code
  - En pratique on repasse en langage semi formel / informel pour faire des démonstrations en maths

---

# Théorie des ensembles ZF

- La vraie base des mathématiques moderne
- Définie à partir de:
  - prédicat d'appartenant $x \in y$ qui est vrai si $x$ est un element de $y$
  - l'axiome d'extentionnalité qui définit l'égalité entre ensembles
    - $\forall A\forall B ((\forall y (y \in A \iff y \in B)) \Rightarrow A = B)$
  - des axiomes de construction
    - axiome de l'ensemble vide $\empty$
    - axiome de la paire
      - Construire des ensembles finis de la forme $\{a_1, a_2, ..., a_n \}$ ou les $a_i$ sont des ensembles
    - axiome de la réunion permettant de construire $A \cup B$ à partir de $A$ et $B$
    - axiome de l'ensemble des parties
    - axiome de l'infini
    - le schéma d'axiome de compréhension
      - Si $A$ est un ensemble et $p$ une formule, permet de construire le sous ensemble $\{ x \in A | p(x) \}$

---

# Arithmétique au sein de la théorie des ensembles

- On peut définir les entiers naturels comme des ensembles
  - $0$ est identifié par l'ensemble vide $\empty$
  - $1$ est identifié par l'ensemble $\{\empty\} = \{0\}$
  - $2$ est identifié par l'ensemble $\{\empty, \{\empty\}\} = \{0, 1\}$
  - $3$ est identifié par l'ensemble $\{\empty, \{\empty\}\, \{\empty, \{\empty\}\}\} = \{0, 1, 2\}$
- De manière générale, $n$ est définit comme l'ensemble $\{0, 1, ..., n - 1 \}$
  - L'opération successeur est donné par: $Sn := n \cup \{ n \}$
  - C'est une construction récursive
- On peut se convaincre que cette construction d'ensemble donne des elements qui respectent les axiomes de Peano
- On dit que la théorie des ensembles contient un modèle de l'arithmétique de Peano
  - Elle est plus générale

---
layout: intro
class: text-center
---

# Cohérence, complétude, décidabilité

---

# Cohérence

- On a vu qu'en maths on formalise tout au sein de théories axiomatiques
- En particulier, la théorie des ensembles nous sert à tout formaliser
- On utilise une série d'axiomes $A_1, A_2, ...$ qu'on considère vrai
  - Cette série peut être infinie, par exemple le schéma d'axiome de compréhension correspond à une infinité d'axiomes permettant de construires l'ensemble $\{ x \in A | p(x) \}$ ou $p(x)$ est une formule quelquonque.
  - Il y a une infinité de formules qu'on peut construire, donc une infinité d'axiome de construction par compréhension
- Mais qu'est ce qui nous prouve que nos axiomes sont **cohérents** entre eux ?
  - C'est à dire qu'ils ne menent pas a une contradiction, une formule qu'on pourrait démontrer vraie et fausse à la fois
  - Ou l'existence d'un objet qui ne respecte pas les axiomes ?

---

# La théorie naïve des ensembles

- La théorie des ensembles naïve contient un schéma d'axiome de compréhension moins restrictif:
  - Pour tout formule $p$, on peut construire l'ensemble $\{ x | p(x) \}$
  - Ce schéma d'axiome permet de construire le paradoxe de Russel qui met la théorie à mal
- Soit la formule $p(x)$ définie par $x \not \in x$, on construit l'ensemble $M = \{ x | p(x) \} = \{ x | x \not \in x \}$
  - Exemple de la vie réelle:
    - L'ensemble des banane n'est pas une banane, donc l'ensemble des bananes n'est pas dans $M$
    - L'ensemble des choses auquelles on peut penser est une chose auquelle on peut penser, donc il est dans $M$
- On cherche a savoir si la formule $M \in M$ est vraie ou fausse
  - Si $M \in M$, alors par définition de $M$, $M \not \in M$
  - Si $M \not \in M$, alors par définition de $M$, $M \in M$
- On arrive à prouver qu'une formule est vraie et fausse à la fois en utilisant cet axiome !
  - La syntaxe nous permet de construire des choses qui n'ont pas de sens

---

# La solution: on restreint l'axiome de compréhension

- On part d'un ensemble existant $A$, d'une formule $p$, et on peut construire $\{ x \in A | p(x) \}$
- $M$ ne peut plus être construit dans ce cadre, car on ne sais pas quoi choisir pour $A$
  - Si on voulait le faire, il faudrait prendre pour $A$: "l'ensemble de tous les ensembles"
  - Mais aucune combinaison d'axiome ne permet de construire "l'ensemble de tous les ensembles"
  - Si cet objet existe, ce n'est pas un ensemble, il n'est donc pas couvert par la théorie des ensembles
- Mais peut-on prouver qu'il n'existe pas d'incohérence sur les axiomes de la théorie ZF des ensembles ?
  - Clairement de la méta-mathématique: on veut prouver qu'on ne peut pas prouver une chose et son contraire
- On dira qu'une théorie est cohérente si elle est sans contradiction

---

# Complétude

- La vérité se confond t-elle avec la prouvabilité ?
- Si une théorie est cohérente, a minima toute formule dérivée des axiomes par un système de déduction valide est vraie, c'est un théorème.
- Mais existe t-il des formules vraie qui ne soit pas dérivable des axiomes ?
- Une formule qui ne peut être déduite, ou sa négation, d'un système d'axiome, est dite indécidable.
  - Cette formule n'entre pas en contradiction avec les axiomes, on peut donc choisir arbitrairement qu'elle soit vraie ou fausse et construire deux autres théories
  - Exemples: axiome du choix, axiome du continu
  - Mais ce n'est pas pareil qu'une formule qui serait vraie, mais non démontrable à partir des axiomes
- Un système formel est dit complet si toute formule vraie y est démontrable

---

# Programme de Hilbert

- Le programme de Hilbert est un programme créé par David Hilbert dans le but d'assurer les fondements des mathématiques (début du 20eme siecle)
- En particulier, tenter de prouver que l'arithmétique formelle des entiers naturel est cohérente et complète
  - Si c'est le cas, on peut entierement automatiser la recherche en mathématique
    - Il suffirait alors d'explorer l'arbre infini des déductions à partir des axiomes pour construire toutes les formules vraies
  - Mais il avait tort, c'est impossible !

---

# Théorème d'incomplétude de Godel

- Si une théorie axiomatique est cohérente et permet de formaliser l'arithmétique, alors elle est incomplète
  - Autrement dit, il existe des formules arithmétiques vraies qu'on ne peut pas démontrer à partir des axiomes de la théorie des ensembles ZF
- Pourrait expliquer pourquoi certaines conjectures ne sont toujours pas démontrées, elles sont peut etre indécidable dans la théorie
  - Exemple: conjecture de Goldbach (tout nombre entier pair superieur à 3 est la somme de deux nombres premiers)
- On ne peut pas entierement automatiser l'exploration des théorèmes mathématiques
  - L'intuition et la créativité sont nécessaires en mathématique
  - La vérité n'est pas équivalente à la prouvabilité
- Encore pire: Godel démontre que l'énoncé "la théorie T est cohérente" est indécidable dans T

---

# Preuve

- Pour la preuve: le livre "Le théorème de Godel" aux éditions Points Sciences
  - Utilise un encodage des formules logiques en formules arithmétiques utilisant des nombres premiers
  - Permet de transformer les méta-mathématiques en arithmétique
  - Un genre de hacking de la logique
