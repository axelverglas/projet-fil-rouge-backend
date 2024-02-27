# Projet Fil Rouge

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- Docker et Docker Compose (pour la base de données MongoDB)
- Python 3.8 ou une version supérieure
- pip pour l'installation des dépendances Python

## Installation

```bash
python -m venv venv
```

```bash
source venv/bin/activate # Sur Windows utilisez `venv\Scripts\activate`
```

```bash
pip install -r requirements.txt
```

## Base de données MongoDB

Pour lancer la base de données MongoDB, exécutez la commande suivante :

```bash
docker-compose up -d
```

## Lancement

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
