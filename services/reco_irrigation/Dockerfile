# 1. On part d'une image officielle Python légère
FROM python:3.9-slim

# 2. On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. On copie le fichier des dépendances
COPY requirements.txt .

# 4. On installe les librairies (sans cache pour garder l'image légère)
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout le reste de ton code dans le conteneur
COPY . .

# 6. On dit au conteneur d'ouvrir le port 8000
EXPOSE 8000

# 7. La commande de démarrage automatique
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]