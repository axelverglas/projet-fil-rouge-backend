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

# Définissez les variables d'environnement nécessaires
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Définissez la commande par défaut pour exécuter votre application
CMD ["flask", "run", "--host=0.0.0.0"]
