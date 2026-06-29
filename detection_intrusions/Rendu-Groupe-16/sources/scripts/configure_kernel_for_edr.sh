#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KERNEL_DIR="${PROJECT_ROOT}/linux-6.18.15"
KCONFIG="${KERNEL_DIR}/.config"

if [[ ! -d "$KERNEL_DIR" ]]; then
  echo "[ERROR] Dossier kernel introuvable: $KERNEL_DIR"
  exit 1
fi

cd "$KERNEL_DIR"

if [[ ! -f "$KCONFIG" ]]; then
  echo "[INFO] .config absent, generation via defconfig"
  make defconfig
fi

scripts/config --file "$KCONFIG" --enable BPF
scripts/config --file "$KCONFIG" --enable BPF_SYSCALL
scripts/config --file "$KCONFIG" --enable BPF_EVENTS
scripts/config --file "$KCONFIG" --enable BPF_JIT
scripts/config --file "$KCONFIG" --enable SECURITY
scripts/config --file "$KCONFIG" --enable BPF_LSM
# BPF LSM programs attach via BPF trampolines on security hooks; that needs
# ftrace (DYNAMIC_FTRACE is selected from FUNCTION_TRACER on x86). Without
# this, bpf_program__attach_lsm() typically fails with -EBUSY (ENODEV busy).
scripts/config --file "$KCONFIG" --enable FUNCTION_TRACER
scripts/config --file "$KCONFIG" --enable DEBUG_INFO
scripts/config --file "$KCONFIG" --enable DEBUG_INFO_DWARF4
scripts/config --file "$KCONFIG" --enable DEBUG_INFO_BTF
scripts/config --file "$KCONFIG" --set-str LSM "landlock,lockdown,yama,integrity,apparmor,bpf"

# Allège fortement le temps de compilation pour une VM QEMU sans affichage
# (edr/scripts/run_vm.sh : -display none, console ttyS0). Inutile de compiler
# DRM, pilotes GPU, son, Wi‑Fi, Bluetooth, USB, média.
# Pour garder un noyau « plein » (ex. GRAPHIC=1, clé USB, Wi‑Fi) :
#   EDR_KERNEL_SLIM=0 bash edr/scripts/configure_kernel_for_edr.sh
if [[ "${EDR_KERNEL_SLIM:-1}" != "0" ]]; then
  scripts/config --file "$KCONFIG" --disable DRM
  scripts/config --file "$KCONFIG" --disable SOUND
  scripts/config --file "$KCONFIG" --disable MEDIA_SUPPORT
  scripts/config --file "$KCONFIG" --disable WIRELESS
  scripts/config --file "$KCONFIG" --disable WLAN
  scripts/config --file "$KCONFIG" --disable BT
  scripts/config --file "$KCONFIG" --disable USB
fi

make olddefconfig </dev/null

if ! command -v pahole >/dev/null 2>&1; then
  echo "[WARN] pahole absent: DEBUG_INFO_BTF peut etre desactive par Kconfig."
else
  echo "[INFO] pahole detecte: $(pahole --version 2>/dev/null || echo unknown)"
fi

echo "[OK] Configuration kernel EDR mise a jour dans: $KCONFIG"
echo "[INFO] Verifie ensuite avec: bash edr/scripts/check_kernel_bpf_lsm.sh \"$KCONFIG\""
