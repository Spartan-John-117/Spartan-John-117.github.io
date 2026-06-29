window.projectData = window.projectData || {};
window.projectData["edr-groupe16"] = {
    title: "EDR Maison — Groupe 16",
    domain: "Détection d'Intrusions",
    technologies: ["C", "eBPF", "Linux Kernel", "Bash"],
    content: `
# Contenu du rendu - Groupe 16

## Arborescence

- \`image/edr-final.qcow2\`
  - Image QCOW2 compressee livrable.
- \`docs/README_UTILISATEUR.md\`
  - Documentation d'utilisation (boot VM, commandes \`edrctl\`, interpretation des alertes).
- \`docs/RAPPORT_CONCEPTION.md\`
  - Rapport de conception.
- \`sources/\`
  - \`bpf/\`
  - \`daemon/\`
  - \`ctl/\`
  - \`include/\`
  - \`scripts/\`
  - \`kernel.config\`

## Verifications rapides

Depuis l'hote:

\`\`\`bash
qemu-img info image/edr-final.qcow2
\`\`\`

Dans la VM:

\`\`\`bash
edrctl status
systemctl status edrd
edrctl block add /bin/ls
/bin/ls
edrctl block add 1.1.1.1
ping -c1 1.1.1.1
edrctl block list
\`\`\`


`
};