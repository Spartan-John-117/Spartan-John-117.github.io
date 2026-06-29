Elevator Basic OS

But du projet
----------------
Ce petit projet Rust implémente une simulation / démonstration d'un "elevator" (ascenseur) pour un petit OS éducatif. 
Il s'agit d'une initiation à Rust et à la programmation bas-niveau dans un contexte d'OS ou d'embarqués.

Contenu et structure
--------------------
- `src/` : code source Rust (point d'entrée `src/main.rs`).
- `Cargo.toml` : manifeste du projet Rust.
- Fichiers de configuration éventuels ou ressources additionnelles dans le dossier racine du projet.

Prérequis
---------
- Rust (version stable recommandée). Installer depuis https://rustup.rs/
- Outil de build `cargo` fourni par l'installation de Rust.

Compilation
-----------
Depuis la racine du dossier du projet (`elevator_basic_os`), exécutez :

```bash
cargo build --release
```

ou en mode debug :

```bash
cargo build
```

Exécution
---------
Pour lancer l'application :

```bash
cargo run --release
```

ou en mode debug :

```bash
cargo run
```

Tests
-----
S'il y a des tests unitaires, lancez-les avec :

```bash
cargo test
```
