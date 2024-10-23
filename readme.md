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
   pip3 install markdown
   ```

## Commandes de build

Pour générer le site, exécutez le script Python principal :

```
python3 generate_site.py
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

- `generate_site.py`: Script principal pour la génération du site
- `*.md`: Fichiers Markdown contenant le contenu des événements
- `*.html`: Fichiers HTML générés
- `styles.css`: Feuille de style CSS pour le site

## Remarques

- Assurez-vous que tous les fichiers Markdown des événements sont dans le même répertoire que le script `generate_site.py`.
- Les images des événements doivent être nommées `evenement-X.webp`, où X est le numéro de l'événement.
- Le fichier CSV contenant les informations des membres du bureau doit être présent dans le répertoire (le nom du fichier est à spécifier dans le script).

Pour toute question ou problème, veuillez contacter les membres du groupe mentionnés ci-dessus.
