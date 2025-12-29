# Étape 1 : Build de l'application (Node.js)
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Utilisation de npm install pour garantir la présence de toutes les dépendances
RUN npm install
COPY . .
RUN npm run build

# Étape 2 : Serveur de production (Nginx)
FROM nginx:alpine
# On copie le build Vite (dossier dist) dans le dossier public de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Important : On crée une config Nginx minimale interne pour écouter sur le port 80
RUN echo 'server { \
    listen 80; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html; \
    try_files $uri $uri/ /index.html; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]