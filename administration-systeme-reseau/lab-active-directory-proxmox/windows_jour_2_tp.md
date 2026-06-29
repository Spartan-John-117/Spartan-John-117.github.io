# TP 2 | Windows Server 2022 – DHCP/DNS + Partage sécurisé + IIS

## Objectifs

```html
<html><body><h1>Intranet [ECOLE_SUPPRIMEE]</h1><p>Serveur : WIN‑SRV01</p></body></html>
```

3. Testez localement sur `http://localhost`

# TP 2 | Windows Server 2022 – DHCP/DNS + Partage sécurisé + IIS

## Objectifs

* Installer et configurer les rôles **DHCP**, **DNS** et **IIS (Web Server)**.
* Mettre en place un **partage de fichiers sécurisé**.
* Administrer à distance un second serveur.
* Déployer un site web interne et mettre en place une redirection.

---

## Partie 1 : Préparation de l’environnement

1. Utilisez les VMs existantes du TP1 : `WIN‑SRV01` (serveur principal) et `WIN‑CLT01` (client).
2. Créez une nouvelle VM `WIN‑SRV02` (voir Partie 6).
3. Assurez-vous que toutes les machines sont sur le réseau `10.99.30.0/24`.
4. Attribuez une IP statique à `WIN‑SRV01` : `10.99.30.10`.

---

## Partie 2 : Installation des rôles sur `WIN‑SRV01`

### 2.1 DHCP

* **GUI** : Server Manager → *Add Roles and Features* → **DHCP Server**
* Activez le **Post-Install configuration**.

### 2.2 DNS

* Ajoutez également le rôle **DNS Server**.

---

## Partie 3 : Configuration DHCP / DNS

### 3.1 DHCP – Scope LAB

| Élément     | Valeur                      |
| ----------- | --------------------------- |
| Plage       | 10.99.30.100 – 10.99.30.200 |
| Masque      | /24                         |
| Passerelle  | 10.99.30.1                  |
| DNS proposé | 10.99.30.10                 |

* Testez depuis `WIN‑CLT01` :
  `ipconfig /release`, `ipconfig /renew`, `ipconfig /all`

### 3.2 DNS

#### Zone directe `lab.local`

| Nom FQDN           | IP          |
| ------------------ | ----------- |
| `srv.lab.local`    | 10.99.30.10 |
| `srv02.lab.local`  | 10.99.30.40 |
| `client.lab.local` | 10.99.30.20 |

#### Zone inversée `30.99.10.in-addr.arpa`

| IP          | PTR              |
| ----------- | ---------------- |
| 10.99.30.10 | srv.lab.local    |
| 10.99.30.20 | client.lab.local |
| 10.99.30.40 | srv02.lab.local  |

#### Alias DNS (CNAME)

* Créez un alias `web.lab.local` → `srv02.lab.local`

---

## Partie 4 : Partage sécurisé (NTFS + SMB)

### 4.1 Comptes & groupe

| Ressource          | Membres / Action       |
| ------------------ | ---------------------- |
| Utilisateurs       | alice, bob, charlie    |
| Groupe `DataUsers` | +alice, +bob, +charlie |

> GUI : `lusrmgr.msc` → *Users & Groups*

### 4.2 Arborescence et droits NTFS

| Dossier                 | Permissions NTFS (héritage coupé)     |
| ----------------------- | ------------------------------------- |
| `C:\Data`               | Admins = Full ; DataUsers = Read/Exec |
| `C:\Data\Alice`         | alice = Full                          |
| `C:\Data\Bob`           | bob = Full                            |
| `C:\Data\Charlie`       | charlie = Full                        |
| `C:\Data\Public` *(RO)* | DataUsers = Read                      |

### 4.3 Partage SMB

| Partage | Chemin    | Droits SMB                                 |
| ------- | --------- | ------------------------------------------ |
| `Data`  | `C:\Data` | DataUsers = Change ; Administrators = Full |

---

## Partie 5 : Ajout du rôle IIS (Web Server)

### 5.1 Installation sur `WIN‑SRV01`

| Méthode | Action                                                           |
| ------- | ---------------------------------------------------------------- |
| **GUI** | Server Manager → *Add Roles and Features* → **Web Server (IIS)** |
| **CLI** | `Install-WindowsFeature Web-Server -IncludeManagementTools`      |

### 5.2 Configuration du site web

1. Allez dans `C:\inetpub\wwwroot`

2. Remplacez `iisstart.htm` par un `index.html` :

```html
<html><body><h1>Intranet [SUPPRIME_2600]</h1><p>Serveur : WIN‑SRV01</p></body></html>
```

3. Testez localement sur `http://localhost`

---

## Partie 6 : Déploiement du second serveur `WIN‑SRV02`

### 6.1 Cloné la VM

| Paramètre | Valeur                     |
| --------- | -------------------------- |
| Nom       | WIN‑SRV02                  |
| RAM       | 4 Go                       |
| Disque    | 40 Go                      |
| IP        | `10.99.30.40`              |
| DNS       | `10.99.30.10` (**SRV01**)  |

### 6.2 Gestion à distance

`WIN‑SRV02` doit être **administrable depuis Server Manager sur `WIN‑SRV01`**, pour permettre l’ajout de rôles ou la surveillance à distance via l’interface graphique.

---

## Partie 7 : Installation d’IIS sur `WIN‑SRV02` à distance

1. Depuis `WIN‑SRV01`, installez le rôle **Web Server (IIS)** sur `WIN‑SRV02` via Server Manager.

2. Modifiez le fichier `index.html` de `WIN‑SRV02` :

```html
<html><body><h1>Site central</h1><p>Serveur : WIN‑SRV02</p></body></html>
```

3. Testez `http://10.99.30.40` depuis `WIN‑CLT01`

---

## Partie 8 : Redirection DNS + HTTP

### 8.1 CNAME DNS

* Créez un alias `web.lab.local` → `srv02.lab.local` dans la zone `lab.local`.

### 8.2 Redirection HTTP

* Objectif : rediriger toute requête vers `http://srv.lab.local` vers `http://srv02.lab.local`
* Modifiez le contenu de `C:\inetpub\wwwroot\index.html` sur `WIN‑SRV01` pour effectuer une redirection HTML permanente (301) :

```html
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0;URL='http://srv02.lab.local'" />
    <title>Redirection</title>
  </head>
  <body>
    <p>Redirection vers le site central...</p>
  </body>
</html>
```

> **Option avancée** (facultatif) : mettre en place une vraie redirection 301 via modification du fichier `web.config` IIS ou via en-têtes HTTP.

### 8.3 Tests

| Test                           | Commande / Interface     | Résultat attendu                   |
| ------------------------------ | ------------------------ | ---------------------------------- |
| Accès à `http://web.lab.local` | Navigateur (`WIN‑CLT01`) | Affiche le site web de `WIN‑SRV02` |
| Accès à `http://srv.lab.local` | Navigateur (`WIN‑CLT01`) | Redirige vers `srv02.lab.local`    |

---

## Partie 9 : Tests finaux

### 9.1 DHCP / DNS

| Test               | Commande                   | Attendu          |
| ------------------ | -------------------------- | ---------------- |
| IP dynamique       | `ipconfig /renew`          | IP entre 100–200 |
| Résolution directe | `nslookup srv02.lab.local` | 10.99.30.40      |
| Résolution inverse | `nslookup 10.99.30.40`     | srv02.lab.local  |

### 9.2 Partage

| Test                          | Résultat attendu |
| ----------------------------- | ---------------- |
| `net use Z: \\WIN‑SRV01\Data` | Accès au partage |
| alice → `Z:\Alice`            | OK               |
| alice → `Z:\Bob`              | Refus            |

### 9.3 Web

| Test                   | Résultat attendu                   |
| ---------------------- | ---------------------------------- |
| `http://10.99.30.10`   | Page locale `WIN‑SRV01` (redirige) |
| `http://10.99.30.40`   | Page IIS de `WIN‑SRV02`            |
| `http://web.lab.local` | Page IIS de `WIN‑SRV02`            |
| `http://srv.lab.local` | Redirection vers `srv02.lab.local` |
