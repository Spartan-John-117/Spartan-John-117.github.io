#!/usr/bin/env bash
set -euo pipefail

KCFG="${1:-/boot/config-$(uname -r)}"

if [[ ! -f "$KCFG" ]]; then
  echo "[ERROR] Kernel config introuvable: $KCFG"
  echo "Passe un chemin en argument, ex: bash scripts/check_kernel_bpf_lsm.sh /path/to/.config"
  exit 1
fi

fail=0

check_flag() {
  local key="$1"
  local expected="$2"
  if grep -q "^${key}=${expected}$" "$KCFG"; then
    echo "[OK] ${key}=${expected}"
  else
    echo "[KO] ${key} doit etre ${expected}"
    fail=1
  fi
}

check_flag "CONFIG_BPF" "y"
check_flag "CONFIG_BPF_SYSCALL" "y"
check_flag "CONFIG_BPF_LSM" "y"
check_flag "CONFIG_FUNCTION_TRACER" "y"
check_flag "CONFIG_DYNAMIC_FTRACE" "y"
check_flag "CONFIG_DEBUG_INFO_BTF" "y"

if grep -q '^CONFIG_LSM="[^"]*bpf[^"]*"$' "$KCFG"; then
  echo "[OK] CONFIG_LSM contient bpf"
else
  echo "[KO] CONFIG_LSM doit contenir bpf"
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "[FAIL] Pre-requis kernel non satisfaits."
  exit 1
fi

echo "[PASS] Pre-requis kernel BPF-LSM valides."
