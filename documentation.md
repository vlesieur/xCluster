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

----------


Utilisation de xCluster
===================
<i class="icon-file"></i> Téléversement d'un fichier
-------------


The document panel is accessible using the <i class="icon-folder-open"></i> button in the navigation bar. You can create a new document by clicking <i class="icon-file"></i> **New document** in the document panel.

<i class="icon-folder-open"></i> Création d'un dossier dans le workspace
-------------

All your local documents are listed in the document panel. You can switch from one to another by clicking a document in the list or you can toggle documents using <kbd>Ctrl+[</kbd> and <kbd>Ctrl+]</kbd>.

<i class="icon-pencil"></i> Modification d'un fichier ou dossier
-------------

You can rename the current document by clicking the document title in the navigation bar.

<i class="icon-trash"></i> Suppression d'un fichier ou dossier
-------------


You can delete the current document by clicking <i class="icon-trash"></i> **Delete document** in the document panel.

<i class="icon-hdd"></i> Export des résultats
-------------

You can save the current document to a file by clicking <i class="icon-hdd"></i> **Export to disk** from the <i class="icon-provider-stackedit"></i> menu panel.

> **Tip:** Check out the [<i class="icon-upload"></i> Publish a document](#publish-a-document) section for a description of the different output formats.


----------


Installation de MongoDB
===================

Télécharger la version community 3.4 à partir de ce lien :

https://www.mongodb.com/download-center?jmp=docs&_ga=1.266151433.748348421.1492676042#community

----------

