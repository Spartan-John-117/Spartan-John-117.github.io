window.projectData = window.projectData || {};
window.projectData["vm-emulation"] = {
    title: "VM Emulation",
    domain: "Développement",
    technologies: ["C", "Architecture Processeur", "Emulation"],
    content: `
# Implémentation — Fonctions VM (instructions et exercices)

À faire :

Il vous est demandé de remplir les lignes précédées par un commentaire \`TODO\`. Il s'agit à chaque fois d'écrire un appel à la fonction \`unpack_from\` du module \`struct\` avec les paramètres adéquats, plus précisément de trouver le bon paramètre \`format\` de cette fonction qui décrit via un jeu de caractères ce qu'il faut lire dans le buffer.

Chaque ligne aura la forme :

\`\`\`
d = struct.unpack_from(XX, buf, pos)
\`\`\`

où il vous suffira de déterminer la valeur appropriée de \`XX\`.

Une lecture et la compréhension de la documentation officielle de Python concernant le module \`struct\` est donc nécessaire pour savoir quelle valeur de \`XX\` est attendue :

https://docs.python.org/3/library/struct.html

Attention : il y a une astuce pour lire la chaîne de caractères basée sur le fait que rien ne vous empêche de créer la valeur de \`XX\` relativement à la valeur d’une autre variable. Autre information, pour lire “une chaîne de caractères” vous devez préciser le “nombre de caractères” de la chaîne suivi du caractère \`s\`. Donc pour lire la chaîne de caractères \`toto\` du buffer \`b'toto'\`, le format à utiliser sera \`4s\`.


- 05 - Écriture de bloc d'octet
--------------------------------
Cet exercice est l'inverse de l'exercice précédent.

À faire :

Il s'agit ici d'écrire la fonction \`encode_opcodes\` qui prend une liste de paires, et génère le flot d'octets correspondant aux informations sémantiques décrites dans la liste de paires. Cette liste de paires est du même type de donnée que celle produite par la fonction \`decode_opcodes\`.

Le code à retrouver est la bonne valeur pour \`XX\` lors de l’appel à la fonction \`struct.pack\` ainsi que le bon passage de paramètre suggéré par \`...\` dans la ligne de code ci-dessous :

\`\`\`python
buf = struct.pack(XX, ...)
\`\`\`

Les paramètres de \`pack\` devront suffire pour encoder le préfixe, la valeur et aussi la taille de la chaîne dans le cas de \`DATASTR\`.


- 06 - Interpréteur et Callable
--------------------------------
Afin de vous préparer au mieux au projet, cet exercice aborde un autre aspect technique utile : l'écriture d'un interpréteur.

Comme vous avez pu le voir lors de l'encodage/décodage de données, tout tourne autour d'une séquence \`if/elif/else\` centrale pour chacun des types de données pris en compte. Que se passe-t-il quand le nombre de types est très important ? La réponse est très souvent un abus de structure de contrôle dite “forêt d'if”, laquelle a tendance à rendre le code moins maintenable.

Pour réaliser un interpréteur, on peut l'implémenter plus joliment en utilisant le concept de \`Callable\`.

Un \`Callable\` est un concept de programmation que l'on retrouve dans de nombreux langages. Ce terme désigne tout type de donnée qui peut stocker une suite d'instructions et d'opérations, et en plus de cela se comporte comme une fonction. Nous pouvons jouer avec cette variable sans savoir quelle fonction elle représente, puis l'appeler.

Il est possible à l’aide de ce genre d'abstraction de solliciter des fonctions sur la base de certaines valeurs. Ici, nous allons enregistrer dans un dictionnaire (type \`dict\`) nommé \`instructions\` les \`Callables\` indexés par la valeur \`OPCODE\` correspondante. Le type énuméré \`OPCODE\` servira dans ce contexte à représenter une instruction de notre machine virtuelle. Les valeurs d’\`OPCODE\` pourront être rapidement cherchées dans ce dictionnaire afin de récupérer la fonction de traitement appropriée et l’appeler.

Ce qui se traduit par la séquence d’instructions :

\`\`\`python
if opcode in instructions:
    instructions[opcode](self)
\`\`\`

En Python, toute fonction est manipulable par son nom (le nom d'une fonction est un \`Callable\`). Il devient donc simple d'écrire un alias pour une fonction :

\`\`\`python
a = print
a("affiche 42")
\`\`\`

Le deuxième type de \`Callable\` que l'on rencontre souvent en Python est la \`lambda\` (fonction anonyme) :

\`\`\`python
a = lambda x, y: x + y
print(a(1, 2))
\`\`\`

Sa syntaxe toutefois est limitée pour éviter les abus, et permet de transformer en fonction uniquement une expression (séquence d'opérations ayant une valeur). Nous faisons la distinction entre “opération” et “instruction” simplement par le fait qu’une opération a une valeur, tandis qu’une instruction n’en a pas.


### Classe, instance et méthode (rappel)

Sans faire un cours complet sur la programmation orientée objet, nous allons utiliser un objet pour cet exercice. Une classe permet de définir un nouveau type de donnée et ses fonctions associées (méthodes). L’ensemble de variables ayant des valeurs propres est appelé un “objet” ou “instance” de la classe. L'instance est accessible par le paramètre \`self\` défini par convention comme étant le premier paramètre de chacune des méthodes.

Exemple rapide :

\`\`\`python
class A:
    def __init__(self, txt):
        self.txt = txt
        self.weight = 0

    def compute_weight(self):
        for c in self.txt:
            self.weight += ord(c)

a = A("test")
print("le poids est", a.weight)
a.compute_weight()
print("le poids est", a.weight)
\`\`\`


### Machine virtuelle Vm (description)

L’objectif de l’exercice est de réaliser une “Machine Virtuelle” (VM) implémentée avec des \`Callables\`. Nous proposons une machine à registre appelée \`Vm\`.


[... Documentation tronquée pour l'affichage ...]
`
};