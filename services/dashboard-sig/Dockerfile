FROM node:18-alpine AS builder

WORKDIR /app

# Copie des fichiers package
COPY package*.json ./

# Installation des dépendances
RUN npm ci

# Copie du code source
COPY . .

# Build de l'application React
RUN npm run build

# Image de production avec nginx
FROM nginx:alpine

# Copie de la configuration nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copie du build Vite (dist au lieu de build)
COPY --from=builder /app/dist /usr/share/nginx/html

# Exposition du port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Démarrage de nginx
CMD ["nginx", "-g", "daemon off;"]
