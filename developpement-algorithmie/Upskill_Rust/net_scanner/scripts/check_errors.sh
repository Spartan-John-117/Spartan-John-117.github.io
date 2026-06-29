#!/usr/bin/env bash
set -euo pipefail

# Script de vérification rapide des messages d'erreur pour net_scanner
# Usage: ./scripts/check_errors.sh [all|name]
# Exécute plusieurs scénarios et vérifie que la sortie stderr contient la chaîne attendue.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/target/debug/net_scanner"

if [ ! -x "$BIN" ]; then
  echo "Binaire non trouvé : $BIN — construction..."
  cargo build
fi

TMPOUT=$(mktemp)
trap 'rm -f "$TMPOUT"' EXIT

run_and_check() {
  local name="$1"
  shift
  local expected="$1"
  shift
  local args=("$@")

  printf "%-30s" "Checking: $name..."

  # Exécute le binaire et capture stdout+stderr
  if "$BIN" "${args[@]}" 2>&1 | tee "$TMPOUT"; then
    status_code=0
  else
    status_code=$?
  fi

  if grep -q -F -- "$expected" "$TMPOUT"; then
    echo "OK"
    return 0
  else
    echo "FAIL"
    echo "--- Sortie ---"
    sed -n '1,120p' "$TMPOUT"
    echo "--- Fin sortie ---"
    return 2
  fi
}

# Si on est root, on saute le test de permission (il réussirait différemment)
IS_ROOT=0
if [ "$(id -u)" -eq 0 ]; then
  IS_ROOT=1
fi

# Scénarios
SCENARIOS=(
  # clap validation déclenche avant notre code; on recherche la mention "invalid value"
  "invalid_protocol|invalid value|--l4_protocol=invalide --dry_run"
  "debug_file_without_format|--debug_file nécessite --debug_format|--debug_file=trace.json --dry_run"
  "invalid_src_mac|Chiffre hexadécimal invalide|--src_mac=zz:zz:zz:zz:zz:zz --dry_run"
  "invalid_ip_bitfield|Valeur hexadécimale invalide|--ip_bitfield=invalide --dry_run"
  "unknown_interface|Interface réseau inconnue|--interface=nonexistent0"
)

EXIT_CODE=0

for s in "${SCENARIOS[@]}"; do
  IFS='|' read -r name expect args_str <<< "$s"
  # split args_str into array
  read -r -a args_arr <<< "$args_str"
  # Si on n'est pas root, l'appel avec --interface tentera d'ouvrir un socket brut
  # et retournera PermissionDenied avant de pouvoir signaler "Interface réseau inconnue".
  if [ "$name" = "unknown_interface" ] && [ "$IS_ROOT" -eq 0 ]; then
    expect="Les privilèges root sont requis"
  fi

  if ! run_and_check "$name" "$expect" "${args_arr[@]}"; then
    EXIT_CODE=$((EXIT_CODE + 1))
  fi
done

# Test permission denied (only if non-root)
if [ "$IS_ROOT" -eq 1 ]; then
  echo "Skipping permission-denied test because running as root"
else
  if ! run_and_check "permission_denied" "Les privilèges root sont requis" --interface=lo; then
    EXIT_CODE=$((EXIT_CODE + 1))
  fi
fi

if [ "$EXIT_CODE" -eq 0 ]; then
  echo "All checks passed"
else
  echo "$EXIT_CODE checks failed"
fi

exit "$EXIT_CODE"
