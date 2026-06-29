window.projectData = window.projectData || {};
window.projectData["lab-proxmox-ad"] = {
    title: "Lab Proxmox Active Directory",
    domain: "Administration Système",
    technologies: ["Proxmox VE", "Windows Server", "Kerberos", "BloodHound"],
    content: `
# TP 1 | Prise en main de la plateforme Proxmox & Installation Windows Server 2022 / Windows 11

## Objectifs

* Découvrir la **plateforme de virtualisation Proxmox VE** mise à disposition.
* Déployer **un serveur Windows Server 2022** et **un poste Windows 11** en appliquant les **bonnes pratiques de virtualisation** (pilotes VirtIO, Qemu Guest Agent, EFI, Secure Boot, snapshots).
* **Activer et sécuriser** les services indispensables (RDP, Windows Update, pare‑feu).
* Manipuler les **outils d’administration locaux** (MMC, PowerShell, Sysinternals) pour valider la configuration.

---

## Partie 1 : Découverte de la plateforme Proxmox VE

### 1.1 Accès & Crédentiels

| Élément                                                   | Valeur                                                      |
| ----------------------                                    | ----------------------------------------------------------- |
| URL                    | \`https://10.99.30.221:8006/\`                                                           |
| Utilisateur            | \`root\`                                                      
                                                            |
| Mot de passe                                            | \`[IDENTIFIANT_SUPPRIMÉ]\`                                                                           |
| Bridge réseau          | \`vmbr0\` ↔ \`10.99.30.0/24\`                                                              |
| **Stockage ISO local** | \`iso\` – contient déjà les ISO Windows & VirtIO pour **éviter la charge réseau**       |

**Étapes :**

1. Connexion via un navigateur.
2. Parcours rapide de l'interface de proxmox.
3. Vérification des ISO (**stockage USI: pour éviter la saturation réseau**) : *Win Server 2022*, *Win 11*, **virtio‑win.iso**.

---

## Partie 2 : Création de la VM Windows Server 2022



### 2.1 Paramètres de la VM

| Paramètre         | Valeur recommandée                        |
| ----------------- | ----------------------------------------- |
| ID / Nom          | \`100\` / \`WIN‑SRV01\`                       |
| Disque système    | 40 Go – VirtIO                            |
| CPU               | 1 sockets × 4 cœurs                       |
| RAM               | 8 Go                                      |
| Réseau            | \`vmbr0\`                                   |
| Options           | **Qemu Guest Agent** activé               |
| Virtio            | virtio-win-0.1.271.iso                    |

### 2.2 Installation
#### Bonnes pratiques
WIN‑CLT01
Pour garantir une installation optimale et conforme aux standards, les bonnes pratiques pour les machines virtuelles Windows sont détaillées dans la documentation officielle de Proxmox VE :  
[Windows guest best practices](https://pve.proxmox.com/wiki/Windows_10_guest_best_practices)

### 3.3 Configuration

| Élément            | Valeur                                |
| ------------------ | ------------------------------------  |
| Nom de la machine  | \`WIN‑SRV01\`                           |
| IPv4               | \`10.99.30.20/24\`                      |
| GWv4               | \`10.99.30.1\`                          |
| DNS                | \`10.99.30.1\`                          |
| RDP                | *Settings → Remote Desktop → Enable*  |
| VirtIO Guest Tools | Installer après premier boot          |

---

## Partie 3 : Création de la VM Windows 11

### 3.1 Paramètres de la VM

| Paramètre         | Valeur recommandée            |
| ----------------- | ----------------------------- |
| ID / Nom          | \`101\` / \`WIN‑CLT01\`           |
| Disque système    | 40 Go – VirtIO                |
| CPU               | 1 sockets × 4 cœurs           |
| RAM               | 8 Go                          |
| Réseau            | \`vmbr0\`                       |
| Options           | **Qemu Guest Agent** activé   |
| Virtio            | virtio-win-0.1.271.iso        |


### 3.2 Installation
#### Bonnes pratiques

Pour garantir une installation optimale et conforme aux standards, les bonnes pratiques pour les machines virtuelles Windows sont détaillées dans la documentation officielle de Proxmox VE :  
[Windows guest best practices](https://pve.proxmox.com/wiki/Windows_10_guest_best_practices)

#### OOBE – BYPASSNRO

**Pourquoi ?** Depuis Windows 11, l’assistant de première ouverture (**OOBE**) impose une connexion Internet et la création d’un compte Microsoft. Dans notre laboratoire hors ligne, cette étape est bloquante. La commande **\`OOBE\BYPASSNRO\`** (By‑Pass Network Requirements Override) relance l’assistant avec des options hors‑ligne, permettant la création d’un compte local et la poursuite de l’installation sans réseau.

Étapes à suivres :
* Démarrer sur l’ISO Windows 11 ; si le disque n’est pas visible, installer les pilotes VirtIO.    
* À l’écran « Se connecter à un réseau », presser **Shift + F10**, taper \`OOBE\BYPASSNRO\`, valider. 
* Sélectionner **Je n’ai pas Internet** puis **Configurer un compte hors ligne**.                  
* Créer votre utilisateur.                                                               

### 3.3 Configuration



[... Documentation tronquée pour l'affichage ...]
`
};