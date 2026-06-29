#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EDR_ROOT="${PROJECT_ROOT}/edr"
ROOTFS_DIR="${EDR_ROOT}/lfs/rootfs"
OVERLAY_DIR="${EDR_ROOT}/lfs/rootfs-overlay"

DIST="${DIST:-noble}"
MIRROR="${MIRROR:-http://archive.ubuntu.com/ubuntu}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "[ERROR] Lance en root (sudo) pour construire le rootfs."
  exit 1
fi

if ! command -v debootstrap >/dev/null 2>&1; then
  echo "[ERROR] debootstrap manquant."
  echo "Installe-le puis relance ce script."
  exit 1
fi

rm -rf "$ROOTFS_DIR"
mkdir -p "$ROOTFS_DIR"

echo "[INFO] Debootstrap $DIST -> $ROOTFS_DIR"
debootstrap --arch=amd64 --variant=minbase "$DIST" "$ROOTFS_DIR" "$MIRROR"

mount --bind /dev "$ROOTFS_DIR/dev"
mount -t proc proc "$ROOTFS_DIR/proc"
mount -t sysfs sys "$ROOTFS_DIR/sys"

cleanup() {
  set +e
  if mountpoint -q "$ROOTFS_DIR/dev"; then umount "$ROOTFS_DIR/dev"; fi
  if mountpoint -q "$ROOTFS_DIR/proc"; then umount "$ROOTFS_DIR/proc"; fi
  if mountpoint -q "$ROOTFS_DIR/sys"; then umount "$ROOTFS_DIR/sys"; fi
}
trap cleanup EXIT

cat > "$ROOTFS_DIR/tmp/edr-rootfs-setup.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y --no-install-recommends \
  systemd-sysv grub-pc iproute2 iputils-ping netcat-openbsd kmod \
  libbpf1 libelf1 zlib1g ca-certificates

echo "edr-vm" > /etc/hostname
cat > /etc/hosts <<'HOSTS'
127.0.0.1 localhost
127.0.1.1 edr-vm
HOSTS

useradd -m -s /bin/bash user || true
echo 'root:root' | chpasswd
echo 'user:user' | chpasswd
EOF

chmod +x "$ROOTFS_DIR/tmp/edr-rootfs-setup.sh"
chroot "$ROOTFS_DIR" /tmp/edr-rootfs-setup.sh
rm -f "$ROOTFS_DIR/tmp/edr-rootfs-setup.sh"

if [[ -d "$OVERLAY_DIR" ]]; then
  cp -a "${OVERLAY_DIR}/." "$ROOTFS_DIR/"
fi

echo "[OK] Rootfs genere dans: $ROOTFS_DIR"
echo "[INFO] Comptes crees: root/root et user/user"
