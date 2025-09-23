# Serveur de Command & Control (C2) avec Python

## Sommaire
1. [Description](#description)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Exécution](#exécution)

## Description
Ce projet met en place un serveur de Command & Control (C2) en Python, capable de se connecter à plusieurs clients afin de leur envoyer des commandes à distance. C'est un outil idéal pour les administrateurs système souhaitant gérer plusieurs machines de manière centralisée. Le serveur offre un menu interactif pour gérer les connexions et envoyer des commandes, tandis que les clients exécutent ces commandes et renvoient les résultats.

### Fonctionnalités Principales
- **Gestion des Connexions** : Accepter et gérer plusieurs connexions de clients.
- **Envoi de Commandes** : Utiliser un menu interactif pour envoyer des commandes à tous les clients ou à un client spécifique.
- **Liste des Clients Connectés** : Afficher les adresses des clients connectés.

## Installation
Avant de commencer, assurez-vous que votre machine a Python 3.x installé. Vous pouvez vérifier cela en exécutant : 
```bash
python3 --version
```
Clonez le dépôt ou téléchargez les fichiers `server.py` et `cible.py`:
```bash
git clone git@github.com:FlavienSR/Serveur-C2_Python.git
cd Serveur-C2_Python
```

## Configuration
Cette section explique comment configurer le serveur et les clients pour un fonctionnement optimal.

### Configuration du Serveur
Le fichier `server.py` est configuré pour démarrer un serveur sur `0.0.0.0:4444`. Vous pouvez modifier ces paramètres si nécessaire. Par défaut, le serveur écoute sur toutes les interfaces réseau disponibles.

### Configuration du Client
Configurez `cible.py` avec les paramètres appropriés pour qu'il puisse se connecter au serveur. Par défaut, il se connecte à `127.0.0.1:4444`.

## Exécution

### Démarrage du Serveur
Pour démarrer le serveur C2, exécutez le script `server.py`. 
**Il faut démarrer le script serveur avant les scripts client !**
```bash
python3 server.py
```

### Connexion d'un Client
Pour connecter un client comme serveur cible, exécutez le script `client.py` sur la machine client.
```bash
python3 cible.py
```

### Interaction
Une fois connecté, utilisez l'interface interactive du serveur:
1. Choisissez `1` pour envoyer une commande à tous les clients.
2. Choisissez `2` pour envoyer une commande à un client spécifique en sélectionnant son numéro.
3. Utilisez `3` pour afficher la liste des clients connectés.
4. Utilisez `4` pour quitter.


Ce projet a été réalisé par FlavienSR
