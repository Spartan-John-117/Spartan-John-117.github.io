# Projet - Turingtoy

L'objectif de ce projet est d'implémenter un interpreteur de machines de Turing.

Votre implémentation doit passer les tests définis dans `tests/tests_turing.py`. Vous pouvez lancer les tests via:

```bash
rye run pytest -k test_turing_machine_double_1 -s
rye run pytest -k test_turing_machine_add_two_binary_numbers -s
rye run pytest -k test_turing_machine_binary_multiplication -s
```

# Instructions

Les tests de `tests/test_turing.py` donnent des informations sur la fonction à implémenter et le format de données.

La fonction à implémenter dans le fichier `src/turingtoy/__init__.py` à la signature suivante:

```python
def run_turing_machine(
    machine: dict[str, Any],
    input_: str,
    steps: int | None = None,
) -> tuple[str, list, bool]
```

La machine de turing est donc représentée par un dictionnaire donc le format est décrit plus bas. Vous pouvez également voir des exemples définis dans les tests, ou en json dans les fichiers sous le dossier `tests/data`.

L'input contient une chaine représentant le contenu de la bande en début d'execution, et la variable `steps` optionelle indique un nombre maximal de transitions à effectuer. Si non spécifié la machine doit être executé jusqu'a blockage, acceptation ou bien tourner à l'infini.

La fonction doit renvoyer un tuple de 3 valeurs:

- Une chaine représentant l'état de la bande en sortie, c'est l'output. Il faudra retirer les symboles vide en début et fin de chaine avant de renvoyer la valeur.
- Un historique d'execution indiquant les états parcourus par la machine et les décisions prise. Vous pouvez consulter les json sous `tests/data` qui donne l'historique d'execution attendu par chaque test.
- Un boolean indiquant si la machine s'est arretée dans un état final (`true`) ou s'est bloqué (`false`, lorsque la machine arrive dans un état qui ne lui permet plus de continuer, sans transition sortante mais non final).

# Format des données

## Machines de Turing

Le format de représentation des MT choisit est similaire à celui utilisé par https://turingmachine.io/ mais exprimé en json (dict en python).

Les champs du dictionnaire sont:

- `blank`: un caractère représentant le symbole vide
- `start state`: une string indiquant l'état initial
- `final states`: une liste de string indiquant les états finaux
- `table`: un dictionnaire représentant la table de transition. Chaque clef est le nom d'un état, et chaque valeur est un dictionnaire.

Le dict associé à un état donne pour chaque symbole lu les instructions à effectuer. Une instruction pour être représentée de deux manière:

- Une chaine `"R"` ou `"L"`, dans ce cas la machine doit simplement aller à droite ou à gauche, sans changer d'état ni rien écrire sur la bande.
- Un dict contenant les champs suivants
  - `write`: un caractère à écrire sur la bande (optional, si non spécifié la machine ne doit rien écrire et laisser le caractère lu)
  - un champs `R` ou `L`: spécifie si la machine doit aller à droite ou à gauche, et indique l'état dans lequel se placer.

Dans les tests, ou utilise une fonction utilitaire `to_dict` pour facilement donner le même comportement à plusieurs états.

Prenons l'exemple suivant, contenu dans la table de la machine du test `test_turing_machine_add_two_binary_numbers`:

```python
"rewrite": {
    "O": {"write": "0", "L": "rewrite"},
    "I": {"write": "1", "L": "rewrite"},
    **to_dict(["0", "1"], "L"),
    " ": {"R": "done"},
},
```

Cette définition indique que si la machine est dans l'état `rewrite`:

- Si elle lit le symbole `O`, elle doit écrire `0`, aller à gauche et se placer dans l'état `rewrite` (ne change pas d'état donc).
- Si elle lit le symbole `I`, elle doit écrire `1`, aller à gauche et se placer dans l'état `rewrite` (ne change pas d'état donc).
- Si elle lit le symbole `0` ou `1`, elle doit simplement aller à gauche sans changer d'état.
- Si elle lit le symbole ` `, elle doit aller à droite et se placer dans l'état `done`.

## Historique d'execution

L'historique d'execution est simplement une liste de dictionnaire contenant les champs suivants:

- `state`: état courant
- `reading`: ce que la machine lit
- `position`: la position de la machine sur le ruban (relatif au champs `memory`)
- `memory`: l'état actuel du ruban (avec symboles vide à gauche et à droite, contrairement à l'output de la machine qui doit être renvoyé)
- `transition`: la transition choisit dans la table (une string ou un dict donc) pour choisir le prochain état et le symbole à écrire.

Un invariant de cette representation doit être `memory[position] == reading`
