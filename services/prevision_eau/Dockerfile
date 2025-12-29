# On utilise une image Python officielle légère
FROM python:3.9-slim

# Force Python à afficher les logs immédiatement
ENV PYTHONUNBUFFERED=1

# Installation des outils système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des requirements
COPY requirements.txt .

# --- OPTIMISATION MAJEURE ---
# 1. On installe d'abord PyTorch version CPU (Léger : ~150Mo au lieu de 2Go)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 2. On installe le reste ensuite (avec un timeout généreux)
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Lancement de l'API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]