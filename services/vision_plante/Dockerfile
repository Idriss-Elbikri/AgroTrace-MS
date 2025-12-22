# 1. Image de base
FROM python:3.10-slim

# 2. Infos (Générique)
LABEL maintainer="AgroTrace Dev Team"

# 3. Dossier de travail
WORKDIR /app

# 4. Installation des dépendances système (Version corrigée pour libgl1)
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# 5. Copie des requirements
COPY requirements.txt .

# 6. Installation des libs Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copie du code
COPY . .

# 8. Port
EXPOSE 8000

# 9. Lancement
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]