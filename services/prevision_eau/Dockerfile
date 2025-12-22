# On utilise une image Python officielle légère
FROM python:3.9-slim

# --- AJOUT CRUCIAL POUR VOIR LES LOGS ---
# Force Python à afficher les prints immédiatement dans la console Docker
ENV PYTHONUNBUFFERED=1

# On installe les outils système nécessaires pour Prophet et Psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# On crée le dossier de travail dans le conteneur
WORKDIR /app

# On copie tes besoins et on les installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout ton code
COPY . .

# Commande de lancement (L'option -u fait la même chose, double sécurité)
CMD ["python", "-u", "main.py"]