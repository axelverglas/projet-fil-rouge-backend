# Utilisez une image Python comme base
FROM python:3.10

# Définissez le répertoire de travail
WORKDIR /app

# Copiez le fichier requirements.txt et installez les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installez Gunicorn
RUN pip install gunicorn

# Copiez tout le reste du projet dans le conteneur
COPY . .

# Définissez les variables d'environnement nécessaires
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Définissez la commande par défaut pour exécuter votre application avec Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]
