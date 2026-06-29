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
| URL                    | `https://10.99.30.221:8006/`                                                           |
| Utilisateur            | `root`                                                      
                                                            |
| Mot de passe                                            | `[IDENTIFIANT_SUPPRIMÉ]`                                                                           |
| Bridge réseau          | `vmbr0` ↔ `10.99.30.0/24`                                                              |
| **Stockage ISO local** | `iso` – contient déjà les ISO Windows & VirtIO pour **éviter la charge réseau**       |

**Étapes :**

1. Connexion via un navigateur.
2. Parcours rapide de l'interface de proxmox.
3. Vérification des ISO (**stockage USI: pour éviter la saturation réseau**) : *Win Server 2022*, *Win 11*, **virtio‑win.iso**.

---

## Partie 2 : Création de la VM Windows Server 2022



### 2.1 Paramètres de la VM

| Paramètre         | Valeur recommandée                        |
| ----------------- | ----------------------------------------- |
| ID / Nom          | `100` / `WIN‑SRV01`                       |
| Disque système    | 40 Go – VirtIO                            |
| CPU               | 1 sockets × 4 cœurs                       |
| RAM               | 8 Go                                      |
| Réseau            | `vmbr0`                                   |
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
| Nom de la machine  | `WIN‑SRV01`                           |
| IPv4               | `10.99.30.20/24`                      |
| GWv4               | `10.99.30.1`                          |
| DNS                | `10.99.30.1`                          |
| RDP                | *Settings → Remote Desktop → Enable*  |
| VirtIO Guest Tools | Installer après premier boot          |

---

## Partie 3 : Création de la VM Windows 11

### 3.1 Paramètres de la VM

| Paramètre         | Valeur recommandée            |
| ----------------- | ----------------------------- |
| ID / Nom          | `101` / `WIN‑CLT01`           |
| Disque système    | 40 Go – VirtIO                |
| CPU               | 1 sockets × 4 cœurs           |
| RAM               | 8 Go                          |
| Réseau            | `vmbr0`                       |
| Options           | **Qemu Guest Agent** activé   |
| Virtio            | virtio-win-0.1.271.iso        |


### 3.2 Installation
#### Bonnes pratiques

Pour garantir une installation optimale et conforme aux standards, les bonnes pratiques pour les machines virtuelles Windows sont détaillées dans la documentation officielle de Proxmox VE :  
[Windows guest best practices](https://pve.proxmox.com/wiki/Windows_10_guest_best_practices)

#### OOBE – BYPASSNRO

**Pourquoi ?** Depuis Windows 11, l’assistant de première ouverture (**OOBE**) impose une connexion Internet et la création d’un compte Microsoft. Dans notre laboratoire hors ligne, cette étape est bloquante. La commande **`OOBE\BYPASSNRO`** (By‑Pass Network Requirements Override) relance l’assistant avec des options hors‑ligne, permettant la création d’un compte local et la poursuite de l’installation sans réseau.

Étapes à suivres :
* Démarrer sur l’ISO Windows 11 ; si le disque n’est pas visible, installer les pilotes VirtIO.    
* À l’écran « Se connecter à un réseau », presser **Shift + F10**, taper `OOBE\BYPASSNRO`, valider. 
* Sélectionner **Je n’ai pas Internet** puis **Configurer un compte hors ligne**.                  
* Créer votre utilisateur.                                                               

### 3.3 Configuration

| Élément            | Valeur                               |
| ------------------ | ------------------------------------ |
| Nom de la machine  | `WIN‑CTL01`                          |
| IPv4               | `10.99.30.30/24`                      |
| GWv4               | `10.99.30.1`                          |
| DNS                | `10.99.30.1`                          |
| RDP                | *Settings → Remote Desktop → Enable* |
| VirtIO Guest Tools | Installer après premier boot         |

---

# Partie 4 – Administration locale & configuration de base

### Objectifs

* Gérer comptes et groupes.
* Administrer les services et partages.
* Automatiser via tâches planifiées.
* Observer le système et appliquer des protections.

---

## 4.1 – Sur le serveur (`WIN‑SRV01`)

---

### Comptes et groupes

* Créer deux utilisateurs :

  * `audit` (admin)
  * `stagiaire` (standard)
* Créer un groupe local `ComptesRestreints`
* Ajouter :

  * `audit` → `Administrators` + `ComptesRestreints`
  * `stagiaire` → `ComptesRestreints`
* Lister tous les comptes et les membres des deux groupes

| Action                   | GUI                              | PowerShell                              |
| ------------------------ | -------------------------------- | --------------------------------------- |
| Créer un utilisateur     | `lusrmgr.msc` → Users → New User | `New-LocalUser`                         |
| Créer un groupe local    | `lusrmgr.msc` → Groups → New     | `New-LocalGroup`                        |
| Ajouter à un groupe      | Groupe → Add                     | `Add-LocalGroupMember`                  |
| Lister comptes / membres | —                                | `Get-LocalUser`, `Get-LocalGroupMember` |

---

### Services & audit

* Passer le service `Print Spooler` en démarrage manuel
* L’arrêter
* Activer :

  * Audit des créations de processus
  * Audit des connexions
* Lancer `notepad.exe`, vérifier l’événement dans le journal `Security`
* Exporter le journal dans `C:\Temp\audit.evtx`

| Action                        | GUI                         | PowerShell / CLI                           |
| ----------------------------- | --------------------------- | ------------------------------------------ |
| Modifier / stopper un service | `services.msc`              | `Set-Service`, `Stop-Service`              |
| Activer audit                 | `gpedit.msc` → Audit Policy | `auditpol`                                 |
| Exporter journal `Security`   | —                           | `wevtutil epl Security C:\Temp\audit.evtx` |

---

### Partages & droits

* Créer `C:\Public` avec des fichiers `.txt`
* Partager le dossier :

  * Lecture seule pour `Everyone`
  * Lecture/écriture pour `audit`
* Appliquer les droits NTFS
* Tester :

  * Accès complet avec `audit`
  * Lecture seule avec `stagiaire`

| Action                   | GUI                             | PowerShell / CLI            |
| ------------------------ | ------------------------------- | --------------------------- |
| Créer / partager dossier | `compmgmt.msc` → Shared Folders | `New-SmbShare`, `net share` |
| Gérer droits NTFS        | Propriétés → Sécurité           | `icacls`, `Set-Acl`         |

---

## 4.2 – Sur le client (`WIN‑CLT01`)

---

### Tâches planifiées

#### **TP\_Logon**

* Déclenchée à chaque ouverture de session
* Exécutée en tant que `SYSTEM`
* Écrit dans `C:\Temp\connection.log` :

  ```
  Utilisateur connecté : <Nom> - <Date>
  ```

#### **TP\_Cleanup**

* Déclenchée chaque dimanche à 12h
* Supprime tous les fichiers de `C:\Windows\Temp`
* Vide la corbeille système

| Tâche                      | GUI            | PowerShell / CLI                                |
| -------------------------- | -------------- | ----------------------------------------------- |
| Créer tâche planifiée      | `taskschd.msc` | `schtasks`, `Register-ScheduledTask`            |
| Log utilisateur connecté   | —              | `Add-Content`, `$env:USERNAME`, `Get-Date`      |
| Nettoyer `C:\Windows\Temp` | —              | `Remove-Item C:\Windows\Temp\* -Force -Recurse` |
| Vider la corbeille         | —              | `Clear-RecycleBin -Force`                       |

---

### Shadow Copy

* Activer les **Shadow Copies** sur le disque système
* Créer une copie manuelle
* Supprimer un fichier dans `C:\Public` (depuis le partage)
* Restaurer ce fichier depuis une **version précédente**

| Action                | GUI                                       | PowerShell / CLI      |
| --------------------- | ----------------------------------------- | --------------------- |
| Activer Shadow Copy   | Propriétés du disque → Shadow Copies      | `vssadmin`, `wbadmin` |
| Restaurer une version | Fichier → clic droit → Restaurer versions | —                     |

---

### Chiffrement EFS

* Créer le dossier `C:\Confidentiel`
* Activer le chiffrement EFS
* Créer un fichier `.txt` à l’intérieur
* Créer un compte local `stagiaire`
* Se connecter avec `stagiaire` et tenter de l’ouvrir
* Exporter le certificat EFS de `audit` au format `.pfx`

| Action                  | GUI                                     | PowerShell / CLI                    |
| ----------------------- | --------------------------------------- | ----------------------------------- |
| Chiffrer un dossier     | Propriétés → Avancé → Cocher "Chiffrer" | `cipher /E`                         |
| Exporter certificat EFS | `certmgr.msc` → Personnel → Exporter    | `Export-PfxCertificate`, `certutil` |

---

### Observation système avec Procmon

* Télécharger et lancer `procmon.exe`
* Filtrer sur le processus `notepad.exe`
* Lancer `notepad.exe` et observer :

  * Ouverture de fichiers
  * Accès au registre
* Sauvegarder les résultats au format `.csv` dans `C:\Temp\trace.csv`

| Action            | GUI / Outil                           | CLI / PowerShell |
| ----------------- | ------------------------------------- | ---------------- |
| Lancer Procmon    | `procmon.exe`                         | —                |
| Appliquer filtres | Filter → Process Name → `notepad.exe` | —                |
| Exporter trace    | File → Save → CSV                     | —                |


## Partie 5 : Extraction de secrets système (SAM / LSA / LSASS / DPAPI)

### Objectifs

* Comprendre les types de secrets stockés localement sur un système Windows.
* Identifier les outils permettant leur extraction ou leur analyse.

### Contenu

Sur la machine `WIN‑SRV01`, il est possible d’extraire des secrets sensibles :

| Élément         | Contenu visé                   | Outils possibles                                      |
| --------------- | ------------------------------ | ----------------------------------------------------- |
| **SAM**         | Hashs des comptes locaux       | `reg save`, **NetExec**, `mimikatz`, `secretsdump.py` |
| **LSA secrets** | MDP de services, clés système  | `reg save`, **NetExec**, `mimikatz`, `secretsdump.py` |
| **LSASS**       | Tickets Kerberos, identifiants | `procdump`, **NetExec**, `mimikatz`                   |
| **DPAPI**       | Secrets protégés (cred Wi-Fi…) | **NetExec**, `mimikatz`, `SharpDPAPI`                 |

---

## Partie 6 : Création d’une VM Windows XP vulnérable (EternalBlue)

### 6.1 Paramètres de la VM

| Paramètre      | Valeur recommandée         |
| -------------- | -------------------------- |
| ID / Nom       | `102` / `WIN‑XP01`         |
| Disque système | 10 Go – IDE                |
| CPU            | 1 socket × 2 cœur         |
| RAM            | 512 Mo                     |
| Réseau         | `vmbr0`                    |
| ISO            | `WINXP`                   |

---

### 6.2 Installation

**Étapes :**

Clé d'installation : V2C47-MK7JD-3R89F-D2KXW-VPK3J

1. Démarrer sur l’ISO Windows XP SP3.
2. Effectuer une installation classique.
3. Vérifier la connectivité réseau entre les machines internes.

### 6.4 Configuration

| Élément            | Valeur                               |
| ------------------ | ------------------------------------ |
| Nom de la machine  | `WIN‑XP01`                          |
| IPv4               | `10.99.30.40/24`                     |
| GWv4               | `10.99.30.1`                         |
| DNS                | `10.99.30.1`                         |

---

### 6.5 Analyse & exploitation (en environnement isolé)

| Usage                             | Outils recommandés              |
| --------------------------------- | ------------------------------- |
| **Détection de la vulnérabilité** | `nmap`, `NetExec` (`nxc`)       |
| **Exploitation de MS17-010**      | `msfconsole` (Metasploit)       |
| **Post-exploitation**             | `meterpreter`, `hashdump`, etc. |
| **Observation réseau**            | `tcpdump`, `wireshark`          |
*
> L’objectif est de **démontrer la présence de la faille** et **valider un accès**, sans aller plus loin dans l’exploitation.

---

### 6.6 Destruction obligatoire

> Cette machine est **volontairement vulnérable**.

* **Supprimez la VM immédiatement après usage**
* Supprimez le **disque associé** dans l’interface Proxmox
* Ne jamais l’exposer à un réseau réel
