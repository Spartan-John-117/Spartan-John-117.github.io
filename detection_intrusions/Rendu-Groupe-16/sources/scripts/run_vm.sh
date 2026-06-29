#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="${PROJECT_ROOT}/edr/output"
KERNEL_IMAGE="${OUTPUT_DIR}/bzImage"
QCOW_IMAGE="${OUTPUT_DIR}/edr.qcow2"

MEMORY_MB="${MEMORY_MB:-4096}"
CPUS="${CPUS:-2}"
GRAPHIC="${GRAPHIC:-0}"
BOOT_MODE="${BOOT_MODE:-disk}"
ROOT_DEV="${ROOT_DEV:-/dev/sda1}"

if [[ ! -f "$QCOW_IMAGE" ]]; then
  echo "[ERROR] Image QCOW2 absente: $QCOW_IMAGE"
  echo "Lance d'abord: bash edr/scripts/build_qcow2.sh (puis finaliser l'installation LFS)"
  exit 1
fi

QEMU_ARGS=(
  -m "$MEMORY_MB"
  -smp "$CPUS"
  -enable-kvm
  -drive "file=${QCOW_IMAGE},format=qcow2"
)

if [[ "$BOOT_MODE" == "kernel" ]]; then
  if [[ ! -f "$KERNEL_IMAGE" ]]; then
    echo "[ERROR] Kernel image absente: $KERNEL_IMAGE"
    echo "Lance d'abord: bash edr/scripts/build_kernel.sh"
    exit 1
  fi
  QEMU_ARGS+=(-kernel "$KERNEL_IMAGE" -append "console=ttyS0 root=${ROOT_DEV} rw")
fi

if [[ "$GRAPHIC" == "1" ]]; then
  QEMU_ARGS+=(-serial mon:stdio)
else
  QEMU_ARGS+=(-display none -monitor none -serial stdio)
fi

echo "[INFO] Boot VM"
echo "[INFO] mode=$BOOT_MODE"
echo "[INFO] kernel=$KERNEL_IMAGE"
echo "[INFO] disk=$QCOW_IMAGE"
exec qemu-system-x86_64 "${QEMU_ARGS[@]}"
