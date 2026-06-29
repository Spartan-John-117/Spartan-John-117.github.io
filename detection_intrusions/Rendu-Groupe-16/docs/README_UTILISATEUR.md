# Mini EDR - Guide complet (build -> VM -> tests)

Ce dossier contient l'implementation du mini EDR impose par le sujet:

- `bpf/` : composant BPF-LSM (`edr.bpf.c`)
- `daemon/` : demon userspace (`edrd`)
- `ctl/` : outil CLI (`edrctl`)
- `include/` : structures partagees
- `scripts/` : scripts de verification et build

## Prerequis

- Build host Linux avec `make`, `gcc/clang`, `libbpf`, `qemu-system-x86_64`.
- Droits root pour les etapes image (`build_rootfs.sh`, `build_qcow2.sh`).
- Se placer a la racine du repo avant les commandes:

```bash
cd /chemin/vers/Kernel/EDR
```

## Etape 1 - Configurer et verifier le noyau

Configurer le noyau avec les options requises BPF-LSM:

```bash
bash edr/scripts/configure_kernel_for_edr.sh
```

Verifier la config produite:

```bash
bash edr/scripts/check_kernel_bpf_lsm.sh linux-6.18.15/.config
```

Options verifiees:

- `CONFIG_BPF=y`
- `CONFIG_BPF_SYSCALL=y`
- `CONFIG_BPF_LSM=y`
- `CONFIG_FUNCTION_TRACER=y`
- `CONFIG_DYNAMIC_FTRACE=y`
- `CONFIG_DEBUG_INFO_BTF=y`
- `CONFIG_LSM` contient `bpf`

## Etape 2 - Compiler kernel + composants EDR

Compiler le noyau:

```bash
bash edr/scripts/build_kernel.sh
```

Compiler les composants EDR:

```bash
make -C edr/bpf
make -C edr/daemon
make -C edr/ctl
```

## Etape 3 - Construire l'image QCOW2

Si besoin, generer le rootfs:

```bash
sudo bash edr/scripts/build_rootfs.sh
```

Construire l'image QCOW2 finale:

```bash
sudo DRY_RUN=0 bash edr/scripts/build_qcow2.sh
```

## Etape 4 - Demarrer la VM

Mode terminal (par defaut):

```bash
bash edr/scripts/run_vm.sh
```

Mode graphique (optionnel):

```bash
GRAPHIC=1 bash edr/scripts/run_vm.sh
```

Boot kernel direct (optionnel):

```bash
BOOT_MODE=kernel ROOT_DEV=/dev/sda1 bash edr/scripts/run_vm.sh
```

## Etape 5 - Verifier le service EDR dans la VM

Connecte en `root`, puis:

```bash
systemctl daemon-reload
systemctl restart edrd
systemctl status edrd
edrctl status
```

Attendu:

- `edrd.service` en `active (running)`
- hooks actifs affiches par `edrctl status`

## Etape 6 - Tests fonctionnels (un seul shell, watch en arriere-plan)

Lancer `edrctl watch` en fond:

```bash
edrctl watch > /tmp/edr-watch.log 2>&1 & WATCH_PID=$!
```

Executer des tests:

```bash
# evenement file_open
cat /etc/hosts

# blocage exec
edrctl block add /bin/ls
/bin/ls

# blocage IP
edrctl block add 1.1.1.1
ping -c1 1.1.1.1
```

Verifier les alertes/events:

```bash
tail -n 80 /tmp/edr-watch.log
edrctl block list
```

Arreter le watcher:

```bash
kill "$WATCH_PID"
```

## Depannage rapide

Si `edrd` ne demarre pas:

```bash
journalctl -u edrd -b --no-pager
```

Si des pins legacy restent presents:

```bash
rm -f /sys/fs/bpf/blocked_exec_paths /sys/fs/bpf/blocked_ipv4
systemctl restart edrd
```