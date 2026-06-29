#!/usr/bin/env bash
set -euo pipefail

# Crée un git bundle prêt à être soumis.
# Usage: ./scripts/make_git_bundle.sh [output-path]
# Exemples:
# ./scripts/make_git_bundle.sh ../net_scanner.bundle
# ./scripts/make_git_bundle.sh net_scanner.bundle

OUT=${1:-net_scanner.bundle}
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

# Vérifier que nous sommes dans un repo git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erreur: ce script doit être exécuté dans la racine d'un dépôt git." >&2
  exit 2
fi

# S'assurer qu'aucun binaire/artefact n'est tracké
echo "Vérification des fichiers trackés indésirables (target, debug.pcap, *.pcap)..."
TRACKED_TARGETS=$(git ls-files | grep -E '(^|/)target(/|$)|\.pcap$' || true)
if [ -n "$TRACKED_TARGETS" ]; then
  echo "Attention: des fichiers/chemins potentiellement volumineux sont suivis par git:" >&2
  echo "$TRACKED_TARGETS" >&2
  echo "Veuillez les supprimer du dépôt avant de créer le bundle (git rm --cached <path>)." >&2
  exit 3
fi

# Vérifier arbre de travail propre
if [ -n "$(git status --porcelain)" ]; then
  echo "L'arbre de travail n'est pas propre. Veuillez committer ou stasher vos modifications avant de créer le bundle." >&2
  git status --porcelain
  exit 4
fi

# Crée le bundle contenant toutes les refs
echo "Création du bundle -> $OUT"
git bundle create "$OUT" --all

# Affiche un résumé
echo "Bundle créé : $OUT"
ls -lh "$OUT" || true
sha256sum "$OUT" || true

echo "Vérifiez le bundle sur une machine propre :"
echo "  mkdir /tmp/repo_test && cd /tmp/repo_test"
echo "  git clone $OUT repo --bare && git clone repo repo_work && cd repo_work && git checkout --detach"

echo "Succès."