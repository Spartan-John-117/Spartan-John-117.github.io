<div align="center">

# Analyseur réseau à socket brut (Rust)

*Construction manuelle des couches L2/L3/L4, génération de traces JSON ou PCAP, exécution en mode simulation ou émission réelle.*

</div>

---

## Aperçu du projet

Ce projet réalise un scanner réseau minimaliste reposant sur un socket brut sous Linux. L’application construit les en-têtes Ethernet, IPv4 et UDP/TCP « à la main », calcule les sommes de contrôle, puis :

- écrit les paquets générés dans un fichier JSON ou PCAP pour inspection, **ou**
- envoie réellement les trames sur l’interface choisie lorsque les privilèges sont suffisants.

L’outil est pensé pour un contexte pédagogique : chaque option exigée par l’énoncé peut être testée de manière indépendante et les sorties sont silencieuses (aucun log sur la console hors erreurs).

## Prérequis

- Linux (socket brut AF_PACKET uniquement disponible/testé sur cette plateforme).
- Rust 1.79 ou supérieur (édition 2021).
- Droits `root` ou capacité `CAP_NET_RAW` si vous souhaitez envoyer des paquets réels.

## Compilation

```bash
cargo build --release
```

Le binaire se trouve ensuite dans `target/release/net_scanner`.

## Utilisation rapide

Simulation complète (aucun paquet émis, trace JSON générée) :

```bash
cargo run -- \
	--src_ip=192.168.1.100 \
	--dst_ip=192.168.1.1 \
	--dest_port=80 \
	--l4_protocol=udp \
	--debug_file=./trace.json \
	--debug_format=json \
	--dry_run
```

Vous pouvez aussi personnaliser la charge utile du paquet via `--payload` :

```bash
cargo run -- --payload "Si ça passait c'était beau." --dry_run
```

Emission réelle sur une interface nommée :

```bash
sudo cargo run -- \
	--src_ip=10.0.0.5 \
	--dst_ip=10.0.0.1 \
	--src_mac=aa:bb:cc:dd:ee:ff \
	--dst_mac=11:22:33:44:55:66 \
	--l4_protocol=tcp \
	--interface=eth0
```

> ℹ️ Sans `--interface`, le programme reste automatiquement en mode simulation, même si `--dry_run` n’est pas fourni.

## Options CLI

| Option | Description |
| ------ | ----------- |
| `--src_ip=<IPv4>` | Adresse source à écrire dans l’en-tête IPv4. |
| `--dst_ip=<IPv4>` | Adresse de destination. |
| `--dest_port=<port>` | Port de destination (UDP/TCP). |
| `--src_mac=<aa:bb:cc:dd:ee:ff>` | Adresse MAC source à injecter dans l’en-tête Ethernet. |
| `--dst_mac=<aa:bb:cc:dd:ee:ff>` | Adresse MAC de destination. |
| `--l4_protocol=<udp|tcp>` | Choix du protocole de couche 4. |
| `--timeout_ms=<ms>` | Délai appliqué après chaque paquet. |
| `--debug_file=<chemin>` | Fichier cible pour les traces. |
| `--debug_format=<json|pcap>` | Format du fichier de traces. |
| `--ip_bitfield=<hex>` | Octet Flags/Fragment IPv4 (ex. `0x04`). |
| `--interface=<nom>` | Interface réseau utilisée pour l’envoi réel. |
| `--dry_run` | Forcer la simulation, aucun paquet n’est émis. |
| `--payload=<string>` | Contenu texte (UTF-8) placé dans la charge utile du paquet. |

Tous les drapeaux listés sont testés individuellement dans le cadre de l’évaluation.

## Formats de traces

- `json` : structure sérialisée contenant les champs L2/L3/L4, la charge utile et les sommes de contrôle. Fichier facile à analyser ou importer dans d’autres outils.
- `pcap` : fichier lisible par Wireshark ou Tshark. Les en-têtes globaux et les horodatages (simples) sont écrits pour chaque paquet.

## Documentation

- Aide embarquée : `cargo run -- --help`
- Documentation HTML :
	```bash
	cargo doc --no-deps --open
	```
	Le point d’entrée se situe dans `target/doc/net_scanner/index.html`.
- Documentation éditoriale : ce fichier `README.md`.

### Extrait d'aide

Voici un extrait de `--help` montrant l'option `--payload` :

```
Usage: net_scanner [OPTIONS]

Options:
			--src_ip <SRC_IP>              Adresse IPv4 source écrite dans l'en-tête IP
			--dst_ip <DST_IP>              Adresse IPv4 de destination pour l'en-tête IP
			--dest_port <DEST_PORT>        Port de destination (couche 4)
			--src_mac <SRC_MAC>            Adresse MAC source utilisée dans l'en-tête Ethernet
			--dst_mac <DST_MAC>            Adresse MAC de destination utilisée dans l'en-tête Ethernet
			--l4_protocol <L4_PROTOCOL>    Choix du protocole de couche 4 pour la sonde [possible values: udp, tcp]
			--timeout_ms <TIMEOUT_MS>      Délai entre les tentatives (en millisecondes)
			--debug_file <DEBUG_FILE>      Chemin du fichier de traces
			--debug_format <DEBUG_FORMAT>  Format du fichier de traces : json ou pcap [possible values: json, pcap]
			--ip_bitfield <IP_BITFIELD>    Valeur brute (8 bits) à injecter dans l'octet Flags/Fragment de l'en-tête IPv4
			--interface <INTERFACE>        Interface réseau à utiliser pour l'envoi réel (optionnelle)
			--dry_run                      N'envoie pas les paquets sur le réseau et se contente d'écrire dans le fichier de traces
			--payload <PAYLOAD>            Contenu (texte) de la payload du paquet
	-h, --help                         Print help
	-V, --version                      Print version
```

## Tests et validation

```bash
cargo fmt
cargo test
```

## Préparer le dépôt pour soumission (git bundle)

Pour soumettre le code sans binaire et avec des builds reproductibles :

1. Assurez-vous d'avoir `rust-toolchain.toml` et `Cargo.lock` committés (déjà présents).
2. Vérifiez que vous n'avez pas de binaires ou d'artefacts trackés (`target/`, `*.pcap`).
3. Utilisez le script fourni pour créer un unique fichier bundle Git :

```bash
chmod +x scripts/make_git_bundle.sh
./scripts/make_git_bundle.sh ../net_scanner.bundle
```

Le script vérifie que l'arbre de travail est propre et qu'aucun artefact volumineux n'est suivi. Il crée `net_scanner.bundle` (ou le chemin que vous fournissez).

Sur la machine de l'évaluateur, le dépôt peut être restauré avec :

```bash
mkdir /tmp/repo_test && cd /tmp/repo_test
git clone /chemin/vers/net_scanner.bundle repo --bare
git clone repo repo_work && cd repo_work
git checkout --detach
```

Notes pour la reproductibilité
- `rust-toolchain.toml` fixe la toolchain (1.79.0).
- `Cargo.lock` est inclus pour verrouiller les versions des dépendances.
- Évitez d'inclure des binaires dans le repository ; le script échouera si des fichiers volumineux sont trackés.


Les tests unitaires valident les conversions de paramètres CLI, la sérialisation PCAP/JSON et les conversions hexadécimales indispensables aux adresses MAC/IP.

## Architecture du code

- `src/main.rs` : définition de la CLI (Clap), point d’entrée et gestion des erreurs utilisateurs.
- `src/scanner.rs` : logique principale, validation des arguments, envoi conditionnel du paquet et orchestration des traces.
- `src/packet.rs` : structures des en-têtes Ethernet/IPv4/UDP/TCP et helpers de calcul (sommes de contrôle, sérialisation binaire).
- `src/debug.rs` : écriture des traces au format JSON ou PCAP.
- `src/error.rs` : type d’erreur unifié et conversions automatiques.

## Limitations connues

- Une seule trame est générée par exécution (pas de boucle multi-cibles).
- Pas de validation approfondie des combinaisons d’options (ex. cohérence IP/MAC dans un même sous-réseau).
- Les horodatages PCAP utilisent des valeurs nulles (0s, 0µs).
