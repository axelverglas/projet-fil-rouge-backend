# Utilisez une image de base officielle de Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel l'application sera disponible
EXPOSE 5000

# Définir la commande pour exécuter l'application
CMD ["flask", "run", "--host=0.0.0.0"]
