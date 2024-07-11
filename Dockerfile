# Utilisez une image Python comme base
FROM python:3.10

# Définissez le répertoire de travail
WORKDIR /app

# Copiez le fichier requirements.txt et installez les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiez tout le reste du projet dans le conteneur
COPY . .

# Définissez les variables d'environnement nécessaires
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Définissez la commande par défaut pour exécuter votre application avec uWSGI
CMD ["flask", "run", "--host=0.0.0.0"]
