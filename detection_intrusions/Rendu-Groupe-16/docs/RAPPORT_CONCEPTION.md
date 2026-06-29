# Rapport de conception - Mini EDR (Groupe 16)

## 1) Repartition des taches

- Membre 1: [kevin.monmouton@ecole2600.com]
- Membre 2: [lucas.joblin@ecole2600.com]
- Membre 3: [antoine.adam@ecole2600.com]
- Membre 4: [boris.trouche@ecole2600.com]

## 2) Ratio de contribution (%)

| Membre | Ratio (%) | Notes |
|---|---:|---|
| Membre 1 | [100] | [100] |
| Membre 2 | [100] | [100] |
| Membre 3 | [100] | [100] |
| Membre 4 | [100] | [100] |

## 3) Choix des hooks BPF-LSM et justification

Les programmes BPF s’attachent aux hooks LSM correspondants (`SEC("lsm/...")`) et s’exécutent dans le chemin de décision sécurité du noyau : on peut soit refuser l’opération (retour négatif, typiquement `-EPERM`), soit laisser passer tout en émettant de la télémétrie via un ring buffer partagé avec le démon utilisateur.

### `bprm_check_security` → programme `edr_bprm_check_security`

Ce hook intervient lors du chargement d’un nouvel exécutable (`execve` et dérivés), avant que le processus ne bascule sur l’image binaire. C’est le point le plus direct pour une politique de **refus d’exécution**.

- **Scénarios d’attaque couverts (détection / blocage)**  
  - **Exécution de malware ou d’outils offensifs** : lancement d’un binaire connu (implant, scanner réseau, exfiltration) déjà identifié par son chemin absolu.  
  - **Persistance par exécution planifiée** : un attaquant ou un script malveillant invoque un binaire placé sous un chemin précis (`cron`, `systemd`, script d’installation). Le blocage par chemin empêche cette chaîne même si le fichier reste sur disque.  
  - **Contournement par copie** : si la politique liste des chemins sensibles (par exemple binaires système rarement légitimes en interactif), toute tentative d’`exec` sur ces chemins est traitée au même titre.  
  - **Chaînes « living off the land » ciblées** : lorsqu’un outil légitime mais dangereux dans un contexte donné est référencé par chemin complet, on peut le bloquer sans toucher aux autres binaires du même nom ailleurs (selon la granularité des clés dans la map).

- **Mécanisme dans notre EDR** : comparaison du chemin fichier (`bprm->filename`) avec une map `blocked_exec_paths` ; en cas de correspondance, émission d’un événement `exec` avec `action=blocked` et retour `-EPERM`. Sinon, journalisation de l’exécution autorisée pour la démonstration (télémétrie des `exec` observés).

### `file_open` → programme `edr_file_open`

Le hook `security_file_open` est invoqué à l’**ouverture** de fichiers (lecture, écriture, selon le contexte noyau). Notre programme ne filtre pas les droits d’ouverture : il sert à la **visibilité** sur les accès, pas au blocage dans cette version.

- **Scénarios d’attaque illustrés par la télémétrie**  
  - **Reconnaissance et vol de données** : lecture de fichiers sensibles (`/etc/shadow`, clés SSH, configurations, bases locales) ; les ouvertures apparaissent avec le nom de fichier court issu du dentry (utile pour corréler avec un comportement suspect).  
  - **Phase « discovery »** : accès répété à des répertoires de configuration ou de secrets avant exfiltration.  
  - **Comportement type ransomware ou outil destructeur** : volume élevé d’ouvertures sur des extensions ou chemins cohérents avec un parcours de fichiers utilisateur (la détection fine dépasse ce mini-EDR, mais le flux d’événements alimente l’analyse).  
  - **Accès à des artefacts de persistance** : ouverture de unités systemd, crontabs, etc., visibles comme séquence d’événements `file_open`.

- **Limite utile à mentionner** : le hook ne reçoit pas le masque d’ouverture (`O_RDONLY`, etc.) dans cette attache LSM telle qu’implémentée ici ; la corrélation se fait surtôt sur **qui** ouvre **quel** inode (nom affiché), pas sur le mode précis.

- **Mécanisme** : pour chaque ouverture autorisée par les hooks précédents, émission d’un événement `file_open` avec `action=allowed` et détail dérivé du dentry.

### `socket_connect` → programme `edr_socket_connect`

Ce hook couvre l’établissement de **connexions sortantes** IPv4 (`connect`). Il est adapté au contrôle d’exfiltration et de **command-and-control** vers des adresses précises.

- **Scénarios d’attaque couverts**  
  - **C2 et balises (beacons)** : le processus malveillant tente `connect()` vers l’IP du serveur de commande ; si l’adresse est en liste noire (`blocked_ipv4`), la tentative échoue avec `-EPERM` et un événement est émis.  
  - **Exfiltration réseau** : transfert vers un relais ou une IP fixe connue (fuites DNS tunneling sortant sont un autre sujet ; ici on cible le cas **IPv4 + connect** classique).  
  - **Mouvement latéral par services réseau** : connexions vers des hômes internes explicitement interdits par politique (segmentation réaffirmée côté endpoint).  
  - **Tests de connectivité abusifs** : `ping`/outils utilisant la stack socket vers une IP bannie (selon l’appel système effectif, le chemin peut passer par ce hook pour une socket IPv4).

- **Mécanisme** : lecture de `sockaddr_in` pour `AF_INET`, lookup de l’adresse (network byte order) dans `blocked_ipv4` ; blocage avec `-EPERM` et journalisation ; sinon événement de connexion autorisée avec l’IP en champ auxiliaire.

### `task_kill` → programme `edr_task_kill`

Le hook concerne l’envoi de signaux pouvant tuer ou interrompre des tâches (`kill`, etc.). Notre implémentation **journalise uniquement** (pas de blocage), ce qui reste utile pour repérer des comportements d’**évasion** ou de **sabotage**.

- **Scénarios d’attaque couverts (détection)**  
  - **Anti-forensics / évitement EDR** : tentative de tuer le démon de journalisation, un agent de sécurité, ou un processus d’investigation.  
  - **Déni de service ciblé** : envoi répété de `SIGKILL` / `SIGTERM` vers des services critiques ou des sessions utilisateur.  
  - **Chaînes d’élévation ou de maintien d’accès** : élimination d’un processus parent ou concurrent avant d’installer une persistance (le signal et la cible `comm` enrichissent le contexte).  
  - **Comportement anormal d’outils légitimes** : scripts ou binaires qui tuent massivement des processus (corrélations possibles avec d’autres événements).

- **Mécanisme** : après succès des vérifications noyau existantes, émission d’un événement avec le `comm` de la cible et le numéro de signal dans les métadonnées.

### `kernel_module_request` → programme `edr_kernel_module_request`

Ce hook est déclenché lorsqu’on demande le chargement d’un **module noyau** par nom (demande explicite de module). C’est une sonde pertinente pour la **confiance envers le noyau** et les extensions chargeables.

- **Scénarios d’attaque couverts (détection)**  
  - **Rootkits ou modules malveillants** : chargement d’un module non standard pour hooker des appels système ou masquer des fichiers/processus.  
  - **Abus de fonctionnalités kernel** : chargement de modules réseau, pare-feu ou périphériques pour étendre les capacités d’un compromis déjà root.  
  - **Persistance au niveau noyau** : bien plus rare que les persistance user-space, mais critique ; la simple **demande** de nom de module laisse une trace avant même un chargement réussi complet selon la politique du système.  
  - **Reconnaissance** : énumération ou déclenchement de chargement automatique pour tester la présence de capacités.

- **Mécanisme** : journalisation du nom de module demandé ; pas de blocage dans cette version (politique « observe d’abord »).

### Synthèse du positionnement

| Hook | Blocage actif | Rôle principal |
|------|---------------|----------------|
| `bprm_check_security` | Oui (`-EPERM`) | Empêcher l’exécution de chemins listés. |
| `file_open` | Non | Visibilité sur les ouvertures de fichiers. |
| `socket_connect` | Oui (`-EPERM`) | Couper les sorties IPv4 vers des IP listées. |
| `task_kill` | Non | Alertes sur les signaux vers d’autres tâches. |
| `kernel_module_request` | Non | Alertes sur les demandes de modules noyau. |

Ce découpage privilégie **deux leviers de refus** (exécution et connectivité IPv4) et **trois canaux de visibilité** (fichiers, signaux, modules), ce qui reste cohérent avec un mini-EDR pédagogique tout en couvrant des familles de menaces distinctes (code malveillant, exfiltration réseau, mouvement sur le système de fichiers, évitement, extension noyau).

## 4) Mecanismes de reponse

On distingue dans ce mini-EDR deux familles de « réponse » : le **refus d’opération** au moment où le noyau l’autoriserait sinon, et la **journalisation** des événements pour analyse ou corrélation. Il n’y a pas de remédiation automatisée avancée (isolement réseau dynamique, terminaison de processus, quarantaine de fichiers) : la conception reste volontairement limitée à des règles statiques et à une trace centralisée.

### 4.1 Réponse préventive : blocage par politique LSM

Lorsqu’une règle s’applique, le programme BPF attaché au hook LSM retourne une erreur négative ; le noyau propage cette erreur à l’appel système (`execve`, `connect`, etc.), ce qui **annule l’effet** de l’opération. L’utilisateur ou le script observe typiquement `Operation not permitted` (`errno = EPERM`).

| Point d’application | Hook | Condition | Effet côté processus |
|---------------------|------|-----------|----------------------|
| Exécution | `bprm_check_security` | Chemin absolu du binaire présent dans la map `blocked_exec_paths` | `execve` échoue ; aucun nouveau programme ne remplace l’image courante. |
| Connectivité IPv4 sortante | `socket_connect` | Adresse IPv4 de destination présente dans la map `blocked_ipv4` | `connect` échoue ; aucune session TCP/UDP n’est établie vers cette IP via ce chemin. |

**Stockage des règles** : les maps BPF sont **épinglées** sous `/sys/fs/bpf/edr/` (pinning par nom). Le contrôle utilisateur (`edrctl block add|del|list`) ouvre ces maps et y insère ou retire des entrées **sans recharger** le bytecode BPF : la politique évolue à chaud tant que le démon tient les maps disponibles.

**Cohérence avec la télémétrie** : dans les deux cas de blocage, un événement est aussi poussé vers le ring buffer avec `action` interprétée côté démon comme `blocked` (valeur `-EPERM` dans le champ `action` de la structure partagée). Ainsi, le refus est à la fois **effectif** (syscall) et **tracé** (journal).

### 4.2 Réponse par visibilité : événements « allowed » et détection

Pour les hooks où aucune liste noire ne s’applique, ou pour les chemins / IP non listés, les programmes BPF retournent `0` : le noyau poursuit le traitement normal. Ils émettent néanmoins des événements avec une action considérée comme **allowed** (tout ce qui n’est pas `-EPERM`). Cela constitue la **réponse par observation** : pas d’interruption, mais enrichissement du journal pour audits, scénarios de démo ou futures règles métier.

- **Exécutions et connexions autorisées** : même sans blocage, `exec` et `socket_connect` produisent une ligne de log (utile pour voir la surface d’activité).  
- **Ouvertures de fichiers, signaux, modules** : ces hooks ne bloquent pas dans notre implémentation ; la « réponse » est entièrement portée par la **collecte** (détection passive).

### 4.3 Chaîne de remontée : noyau → ring buffer → démon → fichier

1. **Noyau** : `bpf_ringbuf_reserve` / `submit` sur la map `events`.  
2. **Démon `edrd`** : consommation via `libbpf` (callback sur le ring buffer), formatage d’une ligne texte (horodatage dérivé de `ts_ns`, PID, UID, `comm`, type d’événement, action `blocked` ou `allowed`, détail, champ auxiliaire — par exemple IP en notation pointée pour `socket_connect`).  
3. **Persistance** : écriture dans `/var/log/edr.log` (et affichage équivalent via `edrctl watch` en suivant le même schéma).

Cette chaîne permet une **réponse organisationnelle** : consulter les logs après coup, corréler avec d’autres sources, ou alimenter un exercice de réponse à incident pédagogique.

### 4.4 Ce que le mini-EDR ne fait pas (périmètre explicite)

- Pas de **kill** ou de **cgroup** imposé par l’EDR en réaction à un événement.  
- Pas de **mise en quarantaine** de fichiers ni de **blocage rétroactif** d’un processus déjà lancé (les refus portent sur la prochaine `execve` ou `connect`).  
- Pas de **remédiation réseau** hors liste d’IPv4 sur `connect` (pas de filtrage DNS, pas d’IPv6 dans cette version).  
- Les règles sont **positives par déni** : seuls les chemins ou IP explicitement listés sont bloqués ; le reste du trafic et des exécutions passe.

En résumé, les **mécanismes de réponse** du projet sont : **(1)** enforcement noyau ciblée par maps BPF sur l’exécution et les connexions IPv4 sortantes, **(2)** journalisation unifiée de tous les types d’événements hookés, **(3)** administration des listes via `edrctl` et visibilité via le journal et `edrctl watch`.

## 5) Scenarios de demonstration reproductibles

Cette section décrit des enchaînements **reproductibles** dans la VM du projet (noyau avec BPF-LSM, service `edrd` actif). Les exemples supposent un shell **root** ou des droits suffisants pour gérer `edrctl` et consulter `/var/log/edr.log`.

### Vue d’ensemble et ordre conseillé

| Ordre | Scénario | Met en avant |
|------|-----------|----------------|
| 1 | C, E (partie télémétrie) | Volume d’événements `allowed`, bruit ambiant, filtrage |
| 2 | D, F (optionnels) | Hooks sans blocage (`task_kill`, `kernel_module_request`) |
| 3 | A, B | Refus noyau `blocked` + corrélation shell / log |
| 4 | E (contraste final) | Rappel : hors liste noire, le trafic et les exec restent journalisés |

Commencer par la **télémétrie** permet de se familiariser avec le format du journal avant d’ajouter des règles qui réduisent volontairement ce qui est « autorisé » côté utilisateur. Les scénarios de **blocage** (A, B) modifient l’état du système (chemins et IP interdits) : les placer en fin de session évite de masquer des étapes ultérieures par erreur (ex. impossible de lancer un outil si son chemin a été bloqué par mégarde).

**Durée indicative** : 10 à 20 minutes pour parcourir A–C avec vérifications ; +5 à 10 minutes avec D, E et F optionnels.

### Prérequis communs

1. **Démon en marche** : `systemctl status edrd` doit indiquer `active (running)` ; `edrctl status` doit afficher `edrd: up` et la liste des hooks (voir section 6).  
2. **Journal disponible** : `edrd` écrit dans `/var/log/edr.log` ; `edrctl watch` ne fait que suivre ce fichier en continu (équivalent pratique pour une démo en direct).  
3. **Format des lignes** (rappel) : chaque événement suit le schéma  
   `ts=… pid=… uid=… comm=… event=<type> action=blocked|allowed detail=… data=…`  
   — pour `socket_connect`, le champ `data=` contient l’IPv4 destination en notation pointée lorsque c’est pertinent.

**Exemple annoté** (les valeurs sont illustratives) :

```text
ts=2026-04-11 14:30:01.123456789 pid=1234 uid=0 comm=ping event=socket_connect action=blocked detail=blocked_ipv4 data=1.1.1.1
```

- `ts` : horodatage dérivé du monotonic `ts_ns` côté noyau, converti en date locale par `edrd`.  
- `pid` / `uid` / `comm` : processus **à l’origine** de l’appel observé (ici le binaire `ping`).  
- `event` : type sémantique (`exec`, `file_open`, `socket_connect`, `task_kill`, `kernel_module_request`).  
- `action` : `blocked` si le BPF a renvoyé l’équivalent de `-EPERM`, sinon `allowed`.  
- `detail` : chaîne libre selon le hook (chemin, nom de fichier court, libellé fixe pour IP bloquée, nom de module, etc.).  
- `data` : IP en notation pointée pour `socket_connect` ; numéro de signal pour `task_kill` lorsque non nul ; parfois `-` si aucune donnée auxiliaire.

**Persistance des règles** : `edrctl block add` insère des clés dans des maps BPF épinglées ; elles **restent** après les tests tant que le noyau ne les efface pas. Le CLI expose `block add` et `block list` **sans** `block del` : pour repartir d’une politique vide en démo, on peut s’appuyer sur une VM réinitialisée, un redémarrage contrôlé du service / de l’environnement, ou un nettoyage manuel des maps (voir le guide utilisateur / dépannage).

### Séquence « un seul terminal » (agrégée)

Pour rejouer rapidement les tests sans multiplier les fenêtres, on peut enchaîner ainsi (après les prérequis) :

```bash
edrctl watch > /tmp/edr-watch.log 2>&1 & WATCH_PID=$!
sleep 1
cat /etc/hosts
/bin/true
ping -c1 9.9.9.9
edrctl block add /bin/ls
/bin/ls || true
edrctl block add 1.1.1.1
ping -c1 1.1.1.1 || true
kill "$WATCH_PID"
grep -E 'event=(exec|socket_connect|file_open)' /tmp/edr-watch.log | tail -n 50
```

Adapter l’ordre si l’on veut observer d’abord uniquement du `allowed` (déplacer les deux `edrctl block add` à la fin). Conserver `|| true` sur les commandes censées échouer évite d’interrompre un script avec `set -e`.

---

### Scénario A — Blocage d’exécution (`bprm_check_security`)

- **Objectif** : montrer qu’un chemin d’exécutable listé est **refusé au moment du `execve`**, avec trace `action=blocked`.  
- **Pourquoi `/bin/ls`** : binaire standard, chemin absolu stable ; l’entrée dans la map doit **exactement** correspondre au chemin vu par le noyau (`bprm->filename`), d’où l’usage du chemin canonique `/bin/ls` plutôt qu’un lien imprévisible.

| Étape | Commande / action | Commentaire |
|------|-------------------|-------------|
| 1 | `edrctl block add /bin/ls` | Ajoute la clé de chemin dans `blocked_exec_paths`. |
| 2 | `edrctl block list` | Vérifie que `/bin/ls` apparaît sous `[blocked paths]`. |
| 3 | `/bin/ls` | Le shell tente `execve` ; le hook LSM renvoie `-EPERM`. |
| 4 | Lecture du journal | `grep 'event=exec' /var/log/edr.log \| tail` ou session `edrctl watch` ouverte avant l’étape 3. |

- **Résultat attendu côté shell** : message du type `bash: /bin/ls: Operation not permitted` (libellé exact selon le shell) ; code de retour non nul.  
- **Résultat attendu côté log** : au moins une ligne avec `event=exec action=blocked` et un `detail=` reflétant le chemin bloqué (chaîne du noyau).  
- **Contrôle négatif utile** : `edrctl block add /usr/bin/ls` **sans** bloquer `/bin/ls` ne bloque pas si l’exécution passe par `/bin/ls` uniquement — cela illustre la granularité **par chaîne de chemin**, pas par inode.  
- **Pièges fréquents** : lancer `ls` sans chemin alors que seul `/bin/ls` est bloqué peut résoudre vers un autre chemin via `PATH` ; pour la démo, préférer **toujours** l’invocation explicite `/bin/ls`.  
- **Après la démo** : tant qu’aucune commande de retrait n’est disponible dans `edrctl`, tout script ou utilisateur qui invoquera encore `/bin/ls` restera bloqué — prévoir un message d’avertissement en présentation orale.

---

### Scénario B — Blocage de connectivité IPv4 sortante (`socket_connect`)

- **Objectif** : montrer le refus d’un `connect()` vers une IPv4 présente dans `blocked_ipv4`, typiquement pour une démo C2 / filtrage sortant.  
- **Note sur `ping`** : selon la version d’`iputils-ping` et le type de socket (ICMP), le noyau peut passer par le hook `socket_connect` lorsque la destination est « connectée » sur le socket ; c’est le cas visé par la démo du sujet. Si une variante locale ne déclenchait pas le hook, un test alternatif est `bash -c 'exec 3<>/dev/tcp/1.1.1.1/443'` ou un petit client Python ouvert avec `connect()` explicite vers la même IP (port ouvert ou non : l’échec attendu reste `EPERM` une fois la règle active).

| Étape | Commande / action | Commentaire |
|------|-------------------|-------------|
| 1 | `edrctl block add 1.1.1.1` | Ajoute l’adresse (format IPv4 dotted-quad). |
| 2 | `edrctl block list` | Vérifie `1.1.1.1` sous `[blocked ipv4]`. |
| 3 | `ping -c1 1.1.1.1` | Trafic sortant vers l’IP bannie (comportement attendu du sujet). |
| 4 | Vérification | Journal ou `edrctl watch` (démarré avant l’étape 3 si besoin). |

- **Résultat attendu côté shell** : échec de la commande avec `Operation not permitted` lorsque l’appel système concerné est bien refusé par LSM.  
- **Résultat attendu côté log** : `event=socket_connect action=blocked`, champ `data=` cohérent avec `1.1.1.1`. Les connexions **non** listées continuent de produire `action=allowed` (télémétrie).  
- **IPv6 / résolution DNS** : une cible atteinte **après** résolution DNS en IPv4 apparaît sous forme d’adresse dans `connect` ; le blocage porte sur l’**adresse**, pas sur le nom d’hôte. Le projet ne traite pas IPv6 dans cette version.  
- **Distinction firewall** : ici le refus est décidé par le programme LSM au moment du `connect` utilisateur ; ce n’est pas une règle `iptables`/`nftables`, ce qui simplifie la démo (une seule politique éditoriale via `edrctl`).

---

### Scénario C — Télémétrie d’ouverture de fichier (`file_open`)

- **Objectif** : illustrer la **visibilité** sans blocage : chaque ouverture pertinente émet un événement `file_open` avec `action=allowed`.  
- **Bruit** : en arrière-plan, d’autres processus ouvrent des fichiers ; filtrer par `comm=` ou par `detail=` aide à isoler son propre test.

| Étape | Commande / action | Commentaire |
|------|-------------------|-------------|
| 1 | `edrctl watch > /tmp/edr-watch.log 2>&1 &` | Capture du flux (ou `tail -f /var/log/edr.log` dans un second terminal). |
| 2 | Attendre la ligne `watching /var/log/edr.log` | Le suiveur est prêt. |
| 3 | `cat /etc/hosts` | Produit des ouvertures côté `cat` (et du bruit possible). |
| 4 | `grep file_open /tmp/edr-watch.log \| tail -n 20` | Recherche des événements `file_open`. |

- **Résultat attendu** : présence d’événements `event=file_open action=allowed` ; le `detail=` reprend le **nom court** issu du dentry (souvent le dernier segment, par ex. `hosts`), pas forcément le chemin absolu complet — comportement aligné sur l’implémentation BPF actuelle.  
- **Variante** : répéter avec un autre fichier (`cat /etc/passwd`) pour montrer la répétition des traces et l’intérêt du filtrage pour l’analyse.  
- **Filtrage pratique** : `grep 'comm=cat.*file_open'` ou `grep 'detail=hosts'` sur le fichier de capture pour isoler son activité ; le bruit système (`systemd`, journaux) peut générer beaucoup de lignes `file_open` — c’est volontairement représentatif d’un poste réel.  
- **Lecture seule vs écriture** : le hook ne distingue pas les modes d’ouverture dans cette version ; la démo porte sur la **présence** d’accès fichier, pas sur l’intention lecture/écriture.

---

### Scénario D — Télémétrie d’envoi de signal (`task_kill`) — optionnel

- **Objectif** : voir un événement `task_kill` avec le numéro de signal dans le champ auxiliaire (`data=`).  
- **Étapes** :  
  1. Lancer un processus long en arrière-plan : `sleep 300 &` noter le PID (`echo $!`).  
  2. Envoyer un signal non létal puis létal : `kill -TERM <PID>` puis `kill -KILL <PID>` si besoin.  
  3. Consulter le journal pour `event=task_kill action=allowed` et le `detail=` correspondant au `comm` de la cible (ex. `sleep`), `data=` reflétant le signal (ex. `15` pour `SIGTERM`).  

Les permissions usuelles Linux s’appliquent (un utilisateur ne peut pas signaler n’importe quelle tâche) ; exécuter en **root** évite ces frictions pour la démo.

---

### Scénario E — Télémétrie « autorisée » exec / réseau (contraste)

- **Objectif** : montrer que les chemins et IP **non** listés génèrent tout de même des événements `allowed`, utile pour la surface d’activité.  
- **Exec** : après s’être assuré que `/bin/true` n’est pas dans la liste des chemins bloqués, exécuter `/bin/true` et vérifier une ligne `event=exec action=allowed`.  
- **Réseau** : `ping -c1 9.9.9.9` (ou toute IPv4 non bloquée) et vérifier `event=socket_connect action=allowed` avec `data=` montrant l’IP contactée.  
- **Comparaison directe** : enchaîner sur la même session un `ping` vers une IP **non** bloquée puis ajouter l’IP à la liste et refaire un `ping` — le journal montre d’abord `allowed`, puis `blocked` pour le même outil (`comm=ping`), ce qui illustre le basculement **sans changer de binaire**.

Ces scénarios complètent A et B en montrant la **double fonction** du composant : refus ciblé **et** journalisation du reste du comportement observé par les hooks.

---

### Scénario F — Télémétrie de demande de module (`kernel_module_request`) — optionnel

- **Objectif** : observer un événement `event=kernel_module_request action=allowed` lorsque le noyau ou un outil utilisateur déclenche une **demande de chargement** de module par nom.  
- **Contexte** : le hook ne garantit pas qu’un module sera effectivement chargé (politique du noyau, signature, modules déjà présents) ; l’intérêt est la **trace** du nom demandé.  
- **Piste de test** (à adapter selon l’image VM et les modules disponibles) : en root, `modprobe <nom>` sur un module présent dans l’arbre des modules mais non chargé, ou toute action applicative qui entraîne un `request_module()` (certaines stacks réseau / périphériques). Si aucun événement n’apparaît, vérifier `journalctl -k` : l’absence de demande explicite explique l’absence de log EDR — ce scénario reste **dépendant de l’environnement**.  
- **Interprétation** : le `detail=` contient le nom de module tel que vu par le hook ; corréler avec les politiques de chargement (`secure boot`, signature des modules, etc.) dépasse le périmètre du mini-EDR mais peut enrichir l’oral.

---

### Check-list de validation (synthèse)

| Scénario | Vérification minimale |
|----------|------------------------|
| A | `Operation not permitted` sur `/bin/ls` + ligne `exec` / `blocked` |
| B | échec de connectivité vers l’IP listée + ligne `socket_connect` / `blocked` et `data=` correct |
| C | au moins un `file_open` / `allowed` avec `detail` cohérent après `cat` ciblé |
| D | `task_kill` / `allowed` avec `data=` = numéro de signal |
| E | `exec` et `socket_connect` en `allowed` hors liste noire |
| F | `kernel_module_request` si l’environnement déclenche une demande |

---

### Dépannage rapide (reproductibilité)

| Symptôme | Piste |
|----------|--------|
| `edrd: down` ou fichier `/run/edrd.status` absent | `systemctl restart edrd` ; consulter `journalctl -u edrd -b --no-pager`. |
| `failed to open ... map` avec `edrctl` | Vérifier que `edrd` a chargé les maps sous `/sys/fs/bpf/edr/` ; pins obsolètes : supprimer `/sys/fs/bpf/blocked_exec_paths` et `/sys/fs/bpf/blocked_ipv4` si présents hors sous-dossier `edr`, puis redémarrer le service (voir README utilisateur). |
| Journal vide ou qui ne grossit pas | Confirmer que le processus `edrd` tourne et que les programmes LSM sont attachés (`edrctl status`) ; générer du trafic (scénario C minimal). |
| Blocage exec / réseau sans événement | Race rare si le journal est plein ou le ring buffer saturé ; sur machine de démo, retenter après quelques secondes ; vérifier espace disque pour `/var/log/edr.log`. |
| `ping` ne déclenche pas le scénario B | Utiliser l’alternative `bash` / `/dev/tcp/` ou un client explicite avec `connect()` vers l’IP bloquée (section B). |

## 6) Commandes de verification

- Etat daemon: `edrctl status`
- Hooks actifs: `edrctl status`
- Regles actives: `edrctl block list`
- Journal temps reel: `edrctl watch`

## 7) Comptes de la LFS

- root:
  - login: `root`
  - mot de passe: [root]
- user:
  - login: `user`
  - mot de passe: [user]