# Sujet de PPD de Master MIAGE FA
## Interface Web pour la Classification Croisée
### Contexte du sujet
Avec l'expansion des volumes de données disponibles, notamment sur le web, la classification ne cesse de
gagner en importance dans le domaine de la science des données pour la réalisation de différentes tâches,
telles que le résumé automatique, l'accélération des moteurs de recherche, l'organisation d'énormes
ensembles de données, etc. Dans ce contexte les méthodes de classification croisée, qui consistent à
partitionner simultanément les lignes et les colonnes d'une matrice, s’avèrent êtres plus avantageuses que les
méthodes de classification simple pour plusieurs raisons telle-que la rapidité et l'interprétation des résultats.
Cependant, contrairement au méthodes de classification simple, très peu d'outils d'analyse de données
implémentent des méthodes de classification croisée et souvent ces outils n'offrent pas d'interface graphique
pour les utilisateurs.
### Travail à effectuer
#### M1
Dans ce PPD on s’intéresse au package python Coclust [1] qui implémente plusieurs méthodes de
classification croisée. L'objectif est de développer une interface web pour Coclust afin de le rendre plus
accessible et plus simple à utiliser. En particulier cette interface devrait permettre :
1. La gestion (création, modification et suppression) d'un répertoire de travail.
2. L'importation de jeux de données sous différents format (.mat, .csv, .txt, .xls, etc.).
3. l’exécution d'une classification croisée sur un jeu de données et récupération des résultats.
4. La visualisation et la sauvegarde des résultats.
Voici un exemple de scenario nominale : l'utilisateur crée un répertoire de travail, il importe ses données, il
applique une classification croisée sur ses données en indiquant (i) la méthode de son choix, (ii) le nombre de
classes lignes et colonnes, (iii) les paramètres spécifiques à l'algorithme choisi.
Le travail à réaliser dans le cadre de ce PPD peut s’inspirer de gCLUTO [2] qui offre une interface graphique
pour la classification simple.
#### M2
Dans la suite de ce PPD, il est demandé de restructurer l'application afin de la rendre davantage maintenable. C'est également l'occasion de rajouter des fonctionnalités. Les points évolutions suivantes sont attendues :
1. Refactorisation du code
2. Utilisation du framework Python Flask
3. Graphique interactif
4. Analyse antivirus
### Outils mis en oeuvre
NodeJS [3], Python, MongoDB [4], zeroMQ [5], AzureAD [6], Node file manager (peut être...) [7]  
### Encadrant : Aghiles Salah (aghiles.salah@parisdescartes.fr).
### Références
+ [1] http://coclust.readthedocs.io/en/latest/index.html
+ [3] http://glaros.dtc.umn.edu/gkhome/cluto/gcluto/overview
+ [3] https://nodejs.org/en/
+ [4] https://www.mongodb.org/
+ [5] http://www.zerorpc.io/ 
+ [6] https://docs.microsoft.com/fr-fr/azure/active-directory/develop/active-directory-devquickstarts-angular , https://azure.microsoft.com/en-us/resources/samples/active-directory-angularjs-singlepageapp/
+ [7] https://github.com/efeiefei/node-file-manager

