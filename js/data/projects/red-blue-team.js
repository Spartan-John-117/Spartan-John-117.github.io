window.projectData = window.projectData || {};
window.projectData["red-blue-team"] = {
    title: "Rapport Red Team / Blue Team",
    domain: "Détection d'Intrusions",
    technologies: ["Splunk", "Sysmon", "PowerShell", "MITRE ATT&CK"],
    content: `
<div align="center">
**Rapport Détection des intrusions**
</div>

<div align="center">Promo 2027 — Groupe 5</div>



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

\`\`\`text
2025-11-07 09:17:21 AR-WIN-DC "powershell.exe" & {Import-Module "C:\AtomicRedTeam\atomics/T1595.003/src/WebServerScan.ps1"

Invoke-WordlistScan -Target "http://localhost" -Wordlist "C:\AtomicRedTeam\atomics/T1595.003/src/wordlist.txt" -Timeout "5" -OutputFile "$env:TMPDIR/wordlist_scan.txt"

Write-Host "Scan complete. Results saved to: $env:TMPDIR/wordlist_scan.txt"}


[... Documentation tronquée pour l'affichage ...]
`
};