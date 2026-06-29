## Protocole Kerberos : échanges détaillés et vulnérabilités associées

### Table des matières

1. Vue d'ensemble
2. Échange AS (Authentication Service)
   - AS-REQ
   - AS-REP
   - Contenu des messages
   - Vulnérabilité : Golden Ticket
3. Échange TGS (Ticket-Granting Service)
   - TGS-REQ
   - TGS-REP
   - Contenu des messages
   - Vulnérabilités : Silver Ticket & Kerberoasting
4. Échange AP (Application Service)
   - AP-REQ
   - AP-REP (optionnel)
   - Contenu des messages
   - Points d'attaque
5. Schémas ASCII des flux Kerberos
6. Conclusion & bonnes pratiques

---

### 1. Vue d'ensemble

Le protocole Kerberos s'appuie sur un tiers de confiance (le KDC, Key Distribution Center) pour authentifier les clients et délivrer des tickets utilisables auprès des services.

- **Client** : machine ou utilisateur qui souhaite accéder à un service.
- **KDC** : composé de deux sous-services :
  - AS (Authentication Service)
  - TGS (Ticket-Granting Service)
- **Service** : ressource (ex. serveur de fichiers) protégée par Kerberos.

L'objectif principal est de ne jamais transmettre de mots de passe en clair et de limiter l'exposition lors de l'authentification.

---

### 2. Échange AS (Authentication Service)

#### a. AS-REQ (Client → KDC)

Contient :

- `realm` (domaine Kerberos)
- `cname` (nom du client)
- `times` (timestamp + durée de validité souhaitée)
- `nonce` (pour liaison de la réponse)
- Optionnel : types de chiffrement supportés

#### b. AS-REP (KDC → Client)

Le KDC répond avec deux parties :

1. **Ticket-Granting Ticket (TGT)**
   - chiffré avec la clé secrète du service KRBTGT
   - Contient :
     - `client ID`, `realm`
     - `session key_c_tgs`
     - `flags`, `times`
2. **Partie Client**
   - chiffrée avec la clé dérivée du mot de passe du client
   - Contient :
     - `session key_c_tgs`
     - `realm`, `nonce`, `times`

> **Golden Ticket** : si un attaquant obtient la clé KRBTGT (hash NTLM du compte KRBTGT), il peut **forcer** la création de n'importe quel TGT valide pour appartenir à n'importe quel utilisateur, bypassant entièrement l'AS.\
> *Exploitation* : Dump du hash KRBTGT (ex. via DCSync), puis génération d'un ticket forgé (ex. Mimikatz)

> **AS-REQ Roasting** : technique où l'attaquant envoie une requête AS-REQ sans pré-authentification (ou avec option `PA_ENC_TIMESTAMP`) pour un compte cible afin de récupérer un AS-REP chiffré avec la clé dérivée du mot de passe de l’utilisateur. Le ticket reçu permet ensuite un brute‑force offline pour retrouver le mot de passe.\
> *Exploitation* : envoi de `AS-REQ` pour un utilisateur existant, capture de l’`AS-REP` (avec Mimikatz ou Impacket) et attaque en bruteforce sur la partie chiffrée du message.

---

### 3. Échange TGS (Ticket-Granting Service)

#### a. TGS-REQ (Client → KDC)

Contient :

- **TGT** reçu précédemment
- **Authenticator** chiffré avec `session key_c_tgs`
  - `cname`, `realm`, `timestamp`
- `service principal name` (SPN) du service visé

#### b. TGS-REP (KDC → Client)

Deux parties :

1. **Service Ticket**
   - chiffré avec la clé secrète du service cible
   - Contient :
     - `client ID`, `realm`
     - `session key_c_s`
     - `flags`, `times`
     - `SPN`
2. **Partie Client**
   - chiffrée avec `session key_c_tgs`
   - Contient le `session key_c_s`, `flags`, `times`

> **Silver Ticket** : si un attaquant connaît la clé secrète (mot de passe) du service cible, il peut forger un **Service Ticket** sans passer par le KDC.\
> *Exploitation* : Dump du hash NTLM d'un compte de service (ex. via mimikatz), forge d'un ticket TGS signé localement.

> **Kerberoasting** : technique offensive où l'attaquant demande un TGS-REP pour un SPN (même sans être admin). Il récupère le ticket chiffré avec la clé du service (généralement RC4) et effectue du brute-force offline sur le hash du mot de passe du compte de service.\
> *Exploitation* : Collecte de tickets via `GetUserSPNs`, extraction et attaque en bruteforce.

---

### 4. Échange AP (Application Service)

#### a. AP-REQ (Client → Service)

Contient :

- **Service Ticket**
- **Authenticator** chiffré avec `session key_c_s`
  - `cname`, `realm`, `timestamp`

#### b. AP-REP (Service → Client, optionnel)

Le service peut répondre pour confirmer l'authentification en renvoyant un Authenticator chiffré avec `session key_c_s`.

##### Points d'attaque possibles :

- **Relecture (Replay)** : utilisation d'un ancien ticket si les timestamps/nonce ne sont pas vérifiés.
- **Pass-the-Ticket** : vol de tickets (TGT ou service tickets) en mémoire et réutilisation sur un autre hôte.

---

### 5. Schémas ASCII des flux Kerberos

```
Client                            KDC              Service
  |-- AS-REQ -------------------->|                                
  |<-- AS-REP (TGT + Part_Cl) ----|                                
  |-- TGS-REQ (TGT + Auth) ------>|                                
  |<-- TGS-REP (ST + Part_Cl) ----|                                
  |-- AP-REQ (ST + Auth) --------------------------->|         
  |<-- AP-REP (Auth) ------------------------------->|         
```

- **TGT** : Ticket-Granting Ticket
- **ST**  : Service Ticket
- **Auth**: Authenticator

---

### 6. Conclusion & bonnes pratiques

- **Sécuriser le compte KRBTGT** : rotation régulière du mot de passe pour limiter fenêtre d'attaque Golden Ticket.
- **Limiter les SPNs exposés** et surveiller les comptes de service pour réduire la surface Kerberoasting.
- **Utiliser AES** plutôt que RC4 pour rendre le brute-force plus difficile.
- **Surveiller les requêtes TGS et AS inhabituellement élevées** et les tickets dignes de suspicion.
- **Implémenter l’authentification multifactorielle** pour réduire l'impact du vol de tickets.

---

