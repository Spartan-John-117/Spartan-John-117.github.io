# Portfolio Cybersécurité

Portfolio personnel hébergé via **GitHub Pages**.

## Déploiement

1. Crée un dépôt nommé `[username].github.io` (remplace `[username]` par ton pseudo GitHub)
2. Place `index.html` à la racine
3. Active GitHub Pages : **Settings → Pages → Source → Deploy from branch → main / root**
4. Ton portfolio sera accessible à `https://[username].github.io`

> Si tu veux l'héberger dans un sous-dossier d'un dépôt existant (ex: `portfolio/`), GitHub Pages peut aussi servir depuis un dossier `/docs` — renomme le dossier `portfolio/` en `docs/` et configure la source en conséquence.

## Personnalisation

Tous les `[placeholders]` sont entre crochets dans `index.html`. Cherche `[` pour les trouver rapidement.

| Placeholder | Contenu |
|---|---|
| `[Ton Nom]` / `[Prénom]` / `[Nom]` | Ton identité |
| `[Pseudo / Initiales]` | Logo nav |
| `[username]` | Ton pseudo GitHub / LinkedIn |
| `[ton@email.fr]` | Ton email |
| `[Titre du projet]` | Tes projets à ajouter |
| `[Nom de ton école / diplôme]` | Ta formation |

## Structure

```
index.html       ← page principale (tout en un seul fichier)
README.md        ← ce fichier
```

Pas de dépendances npm, pas de build step — c'est du HTML/CSS pur avec des polices Google Fonts.
