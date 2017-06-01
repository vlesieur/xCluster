Installation de l'environnement serveur pour xCluster
===================


Ci-dessous nous détaillons comment installer l'environnement pour faire tourner xCluster sur un serveur.

Dans cette procédure nous utilisons une machine sous Windows 10.

L'application est constitué de 2 parties :

- Une partie back en python qui fonctionne en tant que serveur et attend des requêtes du client pour l’exécution des fonctionnalités du package CoClust
- Une partie front en node.js qui est le client du serveur python et enverra les requêtes de l’utilisateur par le biais de l'interface graphique et affichera ensuite les résultats sur cette même interface à la réception du traitement du serveur. 

----------


Installation de ZeroMQ
-------------

Télécharger la dernière version stable de *ZeroMQ* sur leur site internet : http://zeromq.org/distro:microsoft-windows


> **Note:**

> - Dans le cadre d'une production sur un serveur Azure, il peut être difficile d'installer ZeroMQ sans un accès direct/distant à la machine pour l’exécution de l'installeur.
> - Dans notre cas nous travaillons en local sur notre machine.
> 

Installation des composants pour le serveur Python
-------------
> **Prérequis:**

> - Installation de Python version 2.7, nous conseillons de passer par la distribution Anaconda pour avoir tous les composants requis au bon fonctionnement de l'application et de CoClust. 
> La distribution 2.7 de Python est disponible à l'adresse suivante sous la version 4.3 d'Anaconda: https://www.continuum.io/downloads
>

Nous allons maintenant installer les modules node.js requis au déploiement de l'application

Dans un premier temps la librairie python coclust doit être installé pour cela veuillez vous réferer à la documentation d'installation ci-dessous :
http://coclust.readthedocs.io/en/v0.2.0/install.html

Après l'installation de coclust, il faut installer les packages pour l'utilisation de zeroRPC :

>- pip install zerorpc
>- pip install msgpack-python --force-reinstall --upgrade

Installation des composants pour le client Node.js
-------------
> **Prérequis:**

> - Dans un premier nous conseillons activement d'avoir les librairies C++ Visual Studio 2015 et les outils de compilation associés.
Pour cela Microsoft propose un standalone à installer répondant aux prérequis ci-dessus: http://landinghub.visualstudio.com/visual-cpp-build-tools OU exécuter ces commandes :
>- npm install --global --production windows-build-tools
>- npm config set msvs_version 2015
> - Il faut ensuite avoir Node.js installer sur sa machine pour ce faire nous conseillons de télécharger la dernière version stable de Node.js disponible sur leur site internet : https://nodejs.org/en/
>

Nous allons maintenant installer les modules node.js requis au déploiement de l'application

>- npm -g install npm@next
>- npm install -g bower
>- npm install node-gyp
>- npm install zerorpc
>- npm install zmq


----------

Installation de xCluster
===================
> **Prérequis:**

> - Installation de l'environnement serveur
> - Récupération du projet sur Git (git pull)
>

Le lancement et l'arrêt de xCluster se fait par le biais de fichier automatisant ces processus :

**start.vbs** : Permet de lancer tous les serveurs au bon fonctionnement de l'application, au premier démarrage, il sera demandé de fournir le chemin vers le binaire php.exe.
A la fin du processus, l'application se lance sur le navigateur.


**stop.bat** : Permet d'arrêter tous les serveurs.

----------


Utilisation de xCluster
===================

<i class="icon-male"></i> Création d'un compte, connexion et deconnexion
-------------

Dans la page d'accueil de xCluster, une boîte de connexion au centre de la page permet de se connecter à l'application par la saisie de son identifiant (login) et de son mot de passe, le succès de la validation des informations saisies redirige l'utilisateur vers son workspace.

Dans la boite de connexion, un bouton en bas à droite, un lien "Créer un compte" permet d'afficher la boîte d'inscription. La validation des informations saisies connecte directement l'utilisateur vers son workspace.

Sur le workspace, un bouton de deconnexion <i class="icon-off"></i>, en haut à droite de l'écran, permet de se déconnecter.

<i class="icon-folder-open"></i> Création d'un dossier dans le workspace
-------------

Il existe plusieurs méthodes pour créer un dossier dans le workspace :

 - A l'aide de la barre de navigation
 - A l'aide de l'icône dans le dossier courant
 - A l'aide du menu contextuel

<i class="icon-file"></i> Téléversement d'un fichier
-------------

Il existe plusieurs méthodes pour créer un fichier dans un dossier :

 - A l'aide de la barre de navigation
 - A l'aide de l'icône dans le dossier courant
 - A l'aide du menu contextuel
 - Par le biais d'un drag & drop dans la zone d'affichage des fichiers


<i class="icon-pencil"></i> Modification d'un fichier ou dossier
-------------

Pour chaque dossier / fichier, un clique droit permet d'ouvrir un menu contextuel et permet de renommer, modifier un fichier.

<i class="icon-trash"></i> Suppression d'un fichier ou dossier
-------------

Pour chaque dossier / fichier, un clique droit permet d'ouvrir un menu contextuel et permet de supprimer un fichier.

<i class="icon-hdd"></i> Export des résultats
-------------

Lors du traitement des fichiers, les données générées (graphiques, excel) sont automatiquement exportées dans des fichiers dans le dossier courant.
Ces fichiers respecte la politique de nommage suivante :
	**nom_du_fichier**-info-nombre-typeDeDonnées.FormatFichier

Chaque fichier peut ensuite être télécharger à l'aide de l'option dans le menu contextuel.
	

----------


Installation de MongoDB
===================

Télécharger la version community 3.4 à partir de ce lien :

https://www.mongodb.com/download-center?jmp=docs&_ga=1.266151433.748348421.1492676042#community

----------
