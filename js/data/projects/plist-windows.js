window.projectData = window.projectData || {};
window.projectData["plist-windows"] = {
    title: "Visualisateur Processus Windows",
    domain: "Développement",
    technologies: ["C", "Win32 API", "Système Windows"],
    content: `
# PList — Process List (outil de visualisation de processus)

Sujet
-----
PList (Process List) est un utilitaire ligne de commande qui affiche les processus en cours d’exécution sur l’ordinateur local, ainsi que des informations utiles sur chaque processus.

Fonctionnalités attendues
-------------------------
PList affiche :

- Les processus en cours d’exécution sur l’ordinateur, ainsi que leurs ID de processus (PID).
- Détails du processus : utilisation de la mémoire virtuelle.
- Threads en cours d’exécution dans chaque processus, y compris leurs ID de thread.
- En optionnel, détails du processus : la commande dont il émane.
- En optionnel, détails du thread : points d’entrée, la dernière erreur signalée, état du thread.

Comportement / exemples d'utilisation
-------------------------------------
Exemples d'utilisation inspirés de \`pslist.exe\` (SysInternalsSuite) :

1) Aide/usage :

\`\`\`text
z:\> z:\plist.exe -h
[Affiche l'aide et les commandes prises en charge]
\`\`\`

2) Lancer simplement \`plist\` pour voir la liste des processus :

\`\`\`text
z:\> C:\plist.exe
Name        
Idle
System
Registry
smss
csrss
wininit
services
lsass
svchost
fontdrvhost
... (colonnes : Pid Pri Thd Hnd ... Priv CPU Time Elapsed Time)
\`\`\`

3) Filtrer par nom de processus :

\`\`\`text
z:\> Z:\plist.exe explorer
Name
explorer
\`\`\`

4) Détails d'un PID spécifique :

\`\`\`text
z:\> Z:\pslist.exe -d 1160
explorer 1160:
Tid Pri Cswtch ...
State / User Time / Kernel Time / Elapsed Time
... (liste des threads, leurs états et temps CPU)
\`\`\`

Les exemples ci-dessus montrent les données qu'on attend : colonnes pour PID, priorité (Pri), nombre de threads (Thd), handles (Hnd), mémoire privée (Priv), temps CPU (CPU Time), temps écoulé (Elapsed Time), suivi de la liste de threads pour un processus donné, avec leur état et temps utilisateur/kernel.

Objectifs pédagogiques
----------------------
L’objectif de ce projet est de parfaire votre compréhension des domaines suivants :

- API Windows
- Interactions entre l’API Windows et les différentes sphères du système d’exploitation
- Processus, threads et autres modules d’exécution (DLL)

Rendu attendu
--------------
Le rendu se présente sous la forme d’une archive (.zip) contenant l’ensemble des fichiers requis pour la fabrication de votre projet. Est demandé également un fichier \`README.txt\` expliquant les modalités de compilation permettant de construire l’exécutable (\`plist.exe\`).

Dans le fichier \`README.txt\`, vous préciserez aussi la charge de travail des 2 membres du binôme au début de votre fichier. Un cas normal devra ressembler à ceci :

\`\`\`
login_x@ecole2600.com : 50%  login_y@ecole2600.com : 50%
\`\`\`

Le pourcentage sera utilisé pour la notation, donc un binôme fantôme sur le projet (à 0%) aura 0/20. Vous passerez par l’interface de Google Classwork pour déposer ce fichier \`.zip\`.

Références et fonctions utiles (Windows)
--------------------------------------
Pour l’énumération des processus, voir les fonctions suivantes :

- CreateToolhelp32Snapshot
- Process32First
- Process32Next

Pour l’énumération des threads :

- Thread32First
- Thread32Next

Pour plus de détails sur les processus en cours d’exécution, consultez la documentation Windows sur les APIs relatives aux processus et aux threads.



[... Documentation tronquée pour l'affichage ...]
`
};