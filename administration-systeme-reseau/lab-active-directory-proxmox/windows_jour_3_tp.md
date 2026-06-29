# | TP 3 | Active Directory – Architecture complète & résilience

## Objectifs

* Réinitialiser l’environnement : supprimer toutes les VMs existantes sur `npx`, puis recréer `WIN‑CLT01`, `WIN‑SRV01`, `WIN‑SRV02`.
* Promouvoir un **contrôleur de domaine principal**, puis un **secondaire**.
* Structurer l’annuaire avec des **OU**, **utilisateurs**, **groupes** et **GPOs**.
* Gérer les accès RDP via des **groupes AD** centralisés.
* Superviser les **modifications d’objet dans l’annuaire**.
* Tester la **tolérance aux pannes** dans un environnement AD.

---

## Préparation initiale de l’environnement

1. **Supprimer toutes les VMs existantes** sur la plateforme `npx` (via Proxmox).
2. **Recréer les VMs** suivantes avec les IPs statiques suivantes :

| Nom de VM   | IP            | Rôle                            |
| ----------- | ------------- | ------------------------------- |
| `WIN‑SRV01` | `10.99.30.10` | Contrôleur de domaine principal |
| `WIN‑SRV02` | `10.99.30.20` | Second contrôleur de domaine    |
| `WIN‑CLT01` | `10.99.30.30` | Client du domaine               |

> **Passerelle (GW)** : `10.99.30.1`
> **DNS primaire** : `10.99.30.1` (durant la phase d’installation)

---

## Partie 1 : Promotion du domaine principal

1. Sur `WIN‑SRV01` :

   * Installer les rôles **AD DS** et **DNS**.
   * Promouvoir en **nouveau domaine racine** : `ecole.local`.
      * Promouvoir en **nouveau domaine racine** : `ecole.local`.
2. Vérifier :

   * Création automatique des zones DNS
   * Création des conteneurs AD (`Users`, `Computers`, etc.)
   * Résolution DNS interne (ex. : `ping win-srv01.ecole.local`)
      * Résolution DNS interne (ex. : `ping win-srv01.ecole.local`)

---

## Partie 2 : Intégration des machines

1. Sur `WIN‑CLT01` et `WIN‑SRV02` :

   * Joindre les machines au domaine `ecole.local`.
      * Joindre les machines au domaine `ecole.local`.
   * Redémarrer, tester :

     * Résolution DNS interne
     * Présence des objets dans l’annuaire
     * Connexion avec comptes du domaine

---

## Partie 3 : Organisation logique de l’annuaire

### 3.1 Arborescence à créer

```
```
ecole.local
├── Utilisateurs
├── Utilisateurs
│   ├── Etudiants
│   │   ├── L1
│   │   ├── L2
│   │   └── L3
│   └── Staff
│       ├── Enseignants
│       └── Admins
├── Machines
│   ├── Clients
│   └── Serveurs
└── Groupes
```

### 3.2 Utilisateurs

| Login   | Nom complet    | OU                             |
| ------- | -------------- | ------------------------------ |
| alice   | Alice Lemoine  | Utilisateurs\Etudiants\L1      |
| bob     | Bob Garcia     | Utilisateurs\Etudiants\L2      |
| charlie | Charlie Dubois | Utilisateurs\Etudiants\L3      |
| diane   | Diane Martin   | Utilisateurs\Staff\Enseignants |
| edouard | Édouard Petit  | Utilisateurs\Staff\Admins      |

> Mot de passe initial : `P@ssw0rd!`

### 3.3 Groupes de sécurité

Tous les groupes sont créés dans l’OU `Groupes`.

| Groupe           | Membres | Usage                            |
| ---------------- | ------- | -------------------------------- |
| G\_Etudiants\_L1 | alice   | GPO ciblée                       |
| G\_Etudiants\_L2 | bob     | GPO ciblée                       |
| G\_Etudiants\_L3 | charlie | GPO ciblée                       |
| G\_Enseignants   | diane   | Accès distant (RDP)              |
| G\_Admins        | edouard | Délégation + accès distant (RDP) |

### 3.4 Délégation d’administration

1. Créer `gestionnaire_l1` dans `Staff\Admins`.
2. Déléguer à ce compte la gestion de `Etudiants\L1` :

   * Création / suppression d’utilisateurs
   * Réinitialisation des mots de passe

### 3.5 Accès RDP via groupes AD

1. Lier `G_Enseignants` et `G_Admins` au groupe local `Remote Desktop Users` de `WIN‑SRV01`.
2. Ne **rien configurer sur `WIN‑SRV02`**, qui est un serveur Core sans RDP.

---

## Partie 4 : GPO et automatisation

### 4.1 GPO `GPO_Etudiants`

Appliquer cette GPO à l'OU `Etudiants` :

| Paramètre                    | Configuration                                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Interdire `cmd.exe`          | GPO utilisateur > System > Don't run specified Windows applications → `cmd.exe`                                               |
| Interdire `powershell.exe`   | Ajouter `powershell.exe` à la même règle                                                                                      |
| Message légal à la connexion | Computer > Windows Settings > Security Settings > Local Policies > Security Options > Interactive logon: Message text + title |

---

## Partie 5 : Audit et supervision Active Directory

### 5.1 GPO `GPO_Audit_AD` (liée à `Domain Controllers`)

| Catégorie                  | Événements suivis                     |
| -------------------------- | ------------------------------------- |
| Gestion des comptes        | Création / suppression d’utilisateurs |
| Accès à l’annuaire         | Modification des attributs            |
| Changement de mot de passe | Réinitialisation / modification       |

### 5.2 Scénarios à déclencher

1. Créer un utilisateur.
2. Modifier un mot de passe.
3. Supprimer un compte.
4. Déplacer un utilisateur entre OU.

### 5.3 Analyse des journaux (sur `WIN‑SRV02`)

| ID   | Événement                                |
| ---- | ---------------------------------------- |
| 4720 | Création d’un compte utilisateur         |
| 4726 | Suppression d’un compte utilisateur      |
| 4723 | Changement de mot de passe (utilisateur) |
| 4724 | Réinitialisation du mot de passe (admin) |
| 4738 | Modification des propriétés d’un compte  |

Exporter les logs :
`C:\Audit\logins_AD.evtx`

---

## Partie 6 : Mise en place de la résilience

1. Promouvoir `WIN‑SRV02` en **second contrôleur de domaine**.
2. Vérifier la **réplication AD + DNS** entre les DC.
3. Depuis `WIN‑CLT01`, valider que l’annuaire est consultable via `WIN‑SRV02`.

---

## Partie 7 : Test de tolérance aux pannes

1. Éteindre `WIN‑SRV01`.
2. Depuis `WIN‑CLT01` :

   * Se connecter avec un compte du domaine
   * Vérifier la résolution DNS
3. Depuis `WIN‑SRV02` :

   * Créer un utilisateur
4. Rallumer `WIN‑SRV01`, vérifier la réplication