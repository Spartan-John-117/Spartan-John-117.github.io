#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EDR_ROOT="${PROJECT_ROOT}/edr"
OUTPUT_DIR="${EDR_ROOT}/output"
WORK_DIR="${OUTPUT_DIR}/work"
RAW_IMG="${WORK_DIR}/edr.raw"
QCOW2_IMG="${OUTPUT_DIR}/edr.qcow2"
MNT_DIR="${WORK_DIR}/mnt"
ROOTFS_DIR="${ROOTFS_DIR:-${EDR_ROOT}/lfs/rootfs}"
OVERLAY_DIR="${EDR_ROOT}/lfs/rootfs-overlay"
KERNEL_IMAGE="${OUTPUT_DIR}/bzImage"
KERNEL_DIR="${PROJECT_ROOT}/linux-6.18.15"
KERNEL_VERSION="${KERNEL_VERSION:-6.18.15-edr}"

SIZE_GB="${SIZE_GB:-8}"
DRY_RUN="${DRY_RUN:-1}"

mkdir -p "$WORK_DIR"

echo "[INFO] Projet: $PROJECT_ROOT"
echo "[INFO] Sortie: $OUTPUT_DIR"
echo "[INFO] Taille image RAW: ${SIZE_GB}G"
echo "[INFO] Rootfs dir: $ROOTFS_DIR"

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[DRY-RUN] qemu-img create -f raw \"$RAW_IMG\" ${SIZE_GB}G"
  echo "[DRY-RUN] partitionnement + mkfs + copie rootfs local"
  echo "[DRY-RUN] modules_install + grub + artefacts edr"
  echo "[DRY-RUN] qemu-img convert -c -f raw -O qcow2 \"$RAW_IMG\" \"$QCOW2_IMG\""
  echo "[OK] Validation dry-run OK. Passe DRY_RUN=0 pour construire l'image."
  exit 0
fi

if [[ "$(id -u)" -ne 0 ]]; then
  echo "[ERROR] Lance ce script en root (sudo), requis pour loop/mount/grub."
  exit 1
fi

if [[ ! -d "$ROOTFS_DIR" ]]; then
  echo "[ERROR] Rootfs introuvable: $ROOTFS_DIR"
  echo "Lance d'abord: sudo bash edr/scripts/build_rootfs.sh"
  exit 1
fi

if [[ ! -f "$KERNEL_IMAGE" ]]; then
  echo "[ERROR] Kernel image absente: $KERNEL_IMAGE"
  echo "Lance d'abord: bash edr/scripts/build_kernel.sh"
  exit 1
fi

if [[ ! -x "${EDR_ROOT}/daemon/edrd" || ! -x "${EDR_ROOT}/ctl/edrctl" || ! -f "${EDR_ROOT}/bpf/edr.bpf.o" ]]; then
  echo "[ERROR] Artefacts EDR manquants. Build requis:"
  echo "        make -C edr/bpf && make -C edr/daemon && make -C edr/ctl"
  exit 1
fi

loopdev=""
partdev=""

cleanup() {
  set +e
  if mountpoint -q "${MNT_DIR}/dev"; then umount "${MNT_DIR}/dev"; fi
  if mountpoint -q "${MNT_DIR}/proc"; then umount "${MNT_DIR}/proc"; fi
  if mountpoint -q "${MNT_DIR}/sys"; then umount "${MNT_DIR}/sys"; fi
  if mountpoint -q "$MNT_DIR"; then umount "$MNT_DIR"; fi
  if [[ -n "$loopdev" ]]; then losetup -d "$loopdev"; fi
}
trap cleanup EXIT

qemu-img create -f raw "$RAW_IMG" "${SIZE_GB}G"
sfdisk "$RAW_IMG" <<'EOF'
label: dos
unit: sectors

2048,,83,*
EOF

loopdev="$(losetup --find --show --partscan "$RAW_IMG")"
partdev="${loopdev}p1"

mkfs.ext4 -F "$partdev"
mkdir -p "$MNT_DIR"
mount "$partdev" "$MNT_DIR"

cp -a "${ROOTFS_DIR}/." "$MNT_DIR/"

if [[ ! -d "$KERNEL_DIR" ]]; then
  echo "[ERROR] Arbre kernel introuvable: $KERNEL_DIR"
  exit 1
fi

KERNEL_RELEASE="$(make -C "$KERNEL_DIR" -s kernelrelease)"
echo "[INFO] Installation modules kernel -> /lib/modules/${KERNEL_RELEASE}"
make -C "$KERNEL_DIR" -j"$(nproc)" modules
make -C "$KERNEL_DIR" INSTALL_MOD_PATH="$MNT_DIR" modules_install

mkdir -p "$MNT_DIR/boot"
cp -f "$KERNEL_IMAGE" "$MNT_DIR/boot/vmlinuz-${KERNEL_VERSION}"
ln -sf "vmlinuz-${KERNEL_VERSION}" "$MNT_DIR/boot/vmlinuz"

mkdir -p "$MNT_DIR/usr/local/bin" "$MNT_DIR/usr/local/lib/edr"
cp -f "${EDR_ROOT}/daemon/edrd" "$MNT_DIR/usr/local/bin/edrd"
cp -f "${EDR_ROOT}/ctl/edrctl" "$MNT_DIR/usr/local/bin/edrctl"
cp -f "${EDR_ROOT}/bpf/edr.bpf.o" "$MNT_DIR/usr/local/lib/edr/edr.bpf.o"

if [[ -d "$OVERLAY_DIR" ]]; then
  cp -a "${OVERLAY_DIR}/." "$MNT_DIR/"
fi

mkdir -p "$MNT_DIR/var/log" "$MNT_DIR/sys/fs/bpf/edr" "$MNT_DIR/run"
touch "$MNT_DIR/var/log/edr.log"

mkdir -p "$MNT_DIR/etc/udev/rules.d"
cat > "$MNT_DIR/etc/udev/rules.d/99-edr-serial.rules" <<'EOF'
# Optional: tag ttyS* for systemd device units (used by some units).
KERNEL=="ttyS[0-9]*", SUBSYSTEM=="tty", TAG+="systemd"
EOF

mkdir -p "$MNT_DIR/etc/systemd/system"
# serial-getty@ binds to dev-ttyS0.device (often never active with devtmpfs+QEMU).
# Kernel console=ttyS0 makes /dev/console the serial line — console-getty uses that
# and does not wait on dev-ttyS0.device.
ln -sf /dev/null "$MNT_DIR/etc/systemd/system/serial-getty@ttyS0.service"
mkdir -p "$MNT_DIR/etc/systemd/system/getty.target.wants"
ln -sf /lib/systemd/system/console-getty.service \
  "$MNT_DIR/etc/systemd/system/getty.target.wants/console-getty.service"

cat > "$MNT_DIR/etc/systemd/system/edrd.service" <<'EOF'
[Unit]
Description=Mini EDR daemon
After=local-fs.target sysinit.target
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=simple
ExecStartPre=/bin/mkdir -p /sys/fs/bpf
ExecStartPre=/bin/sh -c 'mountpoint -q /sys/fs/bpf || mount -t bpf bpf /sys/fs/bpf'
ExecStartPre=/bin/mkdir -p /sys/fs/bpf/edr
# Stale pinned maps from a crashed run can make the next bpf_object__load fail.
ExecStartPre=/bin/sh -c 'for f in /sys/fs/bpf/edr/*; do [ -e "$f" ] || continue; rm -f "$f"; done'
# Anciens pins à la racine bpffs (avant pin_root_path=/sys/fs/bpf/edr).
ExecStartPre=/bin/rm -f /sys/fs/bpf/blocked_exec_paths /sys/fs/bpf/blocked_ipv4
ExecStart=/usr/local/bin/edrd
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

mkdir -p "$MNT_DIR/etc/systemd/system/multi-user.target.wants"
ln -sf /etc/systemd/system/edrd.service \
  "$MNT_DIR/etc/systemd/system/multi-user.target.wants/edrd.service"

mkdir -p "$MNT_DIR/boot/grub"
cat > "$MNT_DIR/boot/grub/grub.cfg" <<EOF
set timeout=1
set default=0

menuentry "EDR LFS" {
    linux /boot/vmlinuz root=/dev/sda1 rw console=ttyS0,115200n8
}
EOF

mount --bind /dev "$MNT_DIR/dev"
mount -t proc proc "$MNT_DIR/proc"
mount -t sysfs sys "$MNT_DIR/sys"
chroot "$MNT_DIR" depmod -a "$KERNEL_RELEASE"
chroot "$MNT_DIR" grub-install --target=i386-pc --recheck "$loopdev"

sync
umount "$MNT_DIR/dev"
umount "$MNT_DIR/proc"
umount "$MNT_DIR/sys"
umount "$MNT_DIR"
losetup -d "$loopdev"
loopdev=""

qemu-img convert -c -f raw -O qcow2 "$RAW_IMG" "$QCOW2_IMG"

if [[ -n "${SUDO_UID:-}" && -n "${SUDO_GID:-}" ]]; then
  chown "${SUDO_UID}:${SUDO_GID}" "$QCOW2_IMG"
fi
chmod 0644 "$QCOW2_IMG"

echo "[OK] Image creee: $QCOW2_IMG"
