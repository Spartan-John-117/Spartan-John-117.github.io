#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KERNEL_DIR="${PROJECT_ROOT}/linux-6.18.15"
OUTPUT_DIR="${PROJECT_ROOT}/edr/output"

JOBS="${JOBS:-$(nproc)}"

if [[ ! -d "$KERNEL_DIR" ]]; then
  echo "[ERROR] Kernel dir introuvable: $KERNEL_DIR"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

cd "$KERNEL_DIR"

if [[ ! -f ".config" ]]; then
  echo "[ERROR] .config absent. Lance d'abord:"
  echo "        bash edr/scripts/configure_kernel_for_edr.sh"
  exit 1
fi

echo "[INFO] Build kernel linux-6.18.15 (jobs=$JOBS)"
make -j"$JOBS"

cp -f arch/x86/boot/bzImage "${OUTPUT_DIR}/bzImage"
cp -f .config "${OUTPUT_DIR}/kernel.config"

echo "[OK] Kernel compile. Fichiers:"
echo "     ${OUTPUT_DIR}/bzImage"
echo "     ${OUTPUT_DIR}/kernel.config"
