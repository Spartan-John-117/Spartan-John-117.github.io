# Remise à niveau — Puzzles CodinGame

## Puzzles faciles

### `mars_landers_episode_1.py` — Mars Lander

L’objectif de ce programme est de faire atterrir, sans crash, la capsule "Mars Lander" qui contient le rover Opportunity. La capsule “Mars Lander” permettant de débarquer le rover est pilotée par un programme qui échoue trop souvent dans le simulateur de la NASA.


### `the_descent.py` — The Descent

Écrivez le programme permettant de détruire les montagnes pour pouvoir atérir. Pour cela, tirez sur la montagne la plus haute.


### `defibrillators.py` — Defibrillators

La ville de Montpellier a équipé ses rues de défibrillateurs pour permettre de sauver des victimes d'arrêts cardiaques. Les données correspondant à la position de tous les défibrillateurs sont accessibles en ligne. Sur la base des données fournies dans les tests, vous décidez d'écrire un programme qui permettra aux usagers de trouver le défibrillateur le plus proche de là où ils se trouvent, grâce à leur téléphone portable.


### `horse_racing_duals.py` — Horse Racing Duals

L’Hippodrome de Casablanca organise un nouveau type de course de chevaux : les duels. Lors d’un duel, seulement deux chevaux participent à la course. Pour que la course soit intéressante, il faut sélectionner deux chevaux qui ont une puissance similaire. Écrivez un programme qui, à partir d’un ensemble donné de puissances, identifie les deux puissances les plus proches et affiche leur écart avec un nombre entier positif.


### `temperatures.py` — Temperatures

Écrivez un programme qui affiche la température la plus proche de 0 parmi les données d'entrée. Si deux nombres sont aussi proches de zéro, alors l'entier positif sera considéré comme étant le plus proche de zéro (par exemple, si les températures sont -5 et 5, alors afficher 5).


### `unary.py` — Unary

Le binaire avec des 0 et des 1 c'est bien. Mais le binaire avec que des 0, ou presque, c'est encore mieux.

Ecrivez un programme qui, à partir d'un message en entrée, affiche le message codé avec cette technique en sortie.

Règles :
- Le message en entrée est constitué de caractères ASCII (7 bits)
- Le message encodé en sortie est constitué de blocs de 0
- Un bloc est séparé d'un autre bloc par un espace
- Deux blocs consécutifs servent à produire une série de bits de même valeur (que des 1 ou que des 0) :
  - Premier bloc : il vaut toujours 0 ou 00. S'il vaut 0 la série contient des 1, sinon elle contient des 0
  - Deuxième bloc : le nombre de 0 dans ce bloc correspond au nombre de bits dans la série


### `mime_type.py` — Mime Type

Le type MIME est utilisé dans de nombreux protocoles internet pour associer un type de média (html, image, vidéo, ...) avec le contenu envoyé. Ce type MIME est généralement déduit de l'extension du fichier à transférer.

Vous devez écrire un programme qui permet de détecter le type MIME d'un fichier à partir de son nom.


### `ascii_art.py` — Ascii-Art

Dans les gares et aéroports on croise souvent ce type d'écran : Vous êtes-vous demandé comment il serait possible de simuler cet affichage dans un bon vieux terminal ? Nous oui : avec l'art ASCII !

L'art ASCII permet de représenter des formes en utilisant des caractères. Dans notre cas, ces formes sont précisément des mots. Votre mission : Ecrire un programme capable d'afficher une ligne de texte en art ASCII dans un style qui vous est fourni en entrée.

---

## Puzzles moyens

### `stock_exchange_losses.py` — Stock exchange losses

Une entreprise spécialisée dans la finance réalise une étude sur les pires investissements en bourse et souhaite s'équiper pour cela d'un programme. Ce programme devra être capable d'analyser une série chronologique de valeurs d’actions pour afficher la plus grande perte qu'il est possible de réaliser en achetant une action à un instant t0 et en la revendant à une date ultérieure t1. La perte sera exprimée par la différence de valeur entre t0 et t1. S'il n'y a pas de perte, la perte vaudra alors 0.


### `scrabble.py` — Scrabble

Au Scrabble©, chaque lettre est pondéré par un score qui dépend de la difficulté à utiliser cette lettre dans un mot. [...] Le programme doit alors trouver le mot de ce dictionnaire qui rapporte le plus de points pour les sept lettres données (une lettre ne peut être utilisée qu'une seule fois). Si deux mots rapportent le même nombre de points, alors le mot qui apparaît le premier dans le dictionnaire fourni sera choisi.


---

## Comment exécuter les programmes

La plupart des scripts attendent des entrées sur stdin selon l'énoncé du puzzle (format fourni par les tests). Pour lancer un script localement :

```bash
python3 nom_du_script.py < input.txt
```

où `input.txt` contient les entrées de test formatées selon l'énoncé.
