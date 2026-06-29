
# Exercices de TP sur les nombres

Plusieurs exercices sont à réaliser pendant le cours / TP et seront notés.

Ces exercices en python sont à réaliser dans `src/tp_nombres/__init__.py`. Le fichier `tests/test_tp_nombres.py` contient des tests automatiques qui seront utilisés pour vous noter, et ne doit pas être modifié.

Il est interdit d'utiliser des `import` dans le fichier `src/tp_nombres/__init__.py`, tout votre code doit être from scratch.

Vous pouvez lancer un seul test du fichier avec la commande `rye run pytest -k NOM_DU_TEST`.

Dans l'ordre des exercices à faire en TP:

```bash
rye run pytest -k test_nombre_entier
rye run pytest -k test_successeur
rye run pytest -k test_addition
rye run pytest -k test_multiplication
rye run pytest -k test_facto_ite
rye run pytest -k test_facto_rec
rye run pytest -k test_fibo_rec
rye run pytest -k test_fibo_ite
rye run pytest -k test_golden_phi
rye run pytest -k test_sqrt5
rye run pytest -k test_pow
```

Pour débugguer vous pouvez mettre des `print` dans vos tests et lancer avec l'option `-s`, par exemple: `rye run pytest -k test_nombre_entier -s`

Vous pouvez également lancer python en interactif sur le fichier: `rye run python -im tp_nombres.__init__`. Vous pouvez alors appeler vos fonctions.
