FROM python:3.11-slim

# On se place dans le dossier de travail
WORKDIR /service

# On copie les requirements (S'ils sont dans le dossier consumer, on précise le chemin)
COPY ./consumer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- LA CORRECTION EST ICI ---
# Au lieu de copier tout 'consumer' (qui contient 'app'),
# on copie directement le contenu de 'consumer/app' vers '/service/app'
COPY ./consumer/app ./app

# Maintenant, '/service/app' contient directement 'main.py'
# La commande va donc fonctionner :
CMD ["python", "-m", "app.main"]