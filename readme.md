# Vivre aux Lilas - Site Web de l'Association

Ce projet est un générateur de site web statique pour l'association "Vivre aux Lilas". Il utilise Python pour générer des pages HTML à partir de fichiers Markdown et CSV.

## Prérequis système

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation sur Linux

1. Mettez à jour votre système :
   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. Installez Python et pip si ce n'est pas déjà fait :
   ```
   sudo apt install python3 python3-pip -y
   ```

3. Clonez le dépôt (si vous utilisez git) ou téléchargez les fichiers du projet.

4. Naviguez vers le répertoire du projet :
   ```
   cd chemin/vers/le/projet
   ```

5. Installez les dépendances Python :
   ```
   pip3 install -r requirements.txt
   ```

## Dépendances Python

Ce projet utilise les bibliothèques Python suivantes :

- markdown : pour convertir le contenu Markdown en HTML
- csv : (module standard) pour lire les fichiers CSV
- os : (module standard) pour les opérations sur le système de fichiers
- glob : (module standard) pour trouver les fichiers correspondant à un motif
- datetime : (module standard) pour manipuler les dates et heures

Ces dépendances sont listées dans le fichier `requirements.txt` et seront installées automatiquement lors de l'étape 5 de l'installation.

## Commandes de build

Pour générer le site, exécutez le script Python principal :

```
python3 main.py
```

Ce script va :
- Générer la page des membres du bureau à partir d'un fichier CSV
- Créer la page d'accueil avec les actualités
- Générer les pages individuelles pour chaque événement
- Créer la page listant tous les événements

## Membres du groupe

- Dorian D.
- Thomas A.

## Structure du projet

- `main.py`: Script principal pour la génération du site
- `*.md`: Fichiers Markdown contenant le contenu des événements
- `*.html`: Fichiers HTML générés
- `styles.css`: Feuille de style CSS pour le site

## Vscode live server

```
"liveServer.settings.port": 5501,
"liveServer.settings.root": "/public"
```

## Remarques

- Assurez-vous que tous les fichiers Markdown des événements sont dans le même répertoire que le script `main.py`.
- Les images des événements doivent être nommées `evenement-X.webp`, où X est le numéro de l'événement.
- Le fichier CSV contenant les informations des membres du bureau doit être présent dans le répertoire (le nom du fichier est à spécifier dans le script).

Pour toute question ou problème, veuillez contacter les membres du groupe mentionnés ci-dessus.
