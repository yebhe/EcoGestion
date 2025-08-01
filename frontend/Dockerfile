# Dockerfile pour Vue.js - Alternative
FROM node:18-alpine as build-stage

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le code source
COPY . .

# Modifier temporairement vite.config.js pour Docker
RUN sed -i "s|outDir: '../backend/static/build'|outDir: 'dist'|g" vite.config.js

# Vérifier la modification
RUN echo "=== Configuration Vite modifiée ===" && \
    grep -A 5 -B 5 "outDir" vite.config.js

# Construire l'application
RUN npm run build

# Vérifier le build
RUN echo "=== Contenu après build ===" && \
    ls -la dist/ && \
    echo "=== Quelques fichiers ===" && \
    find dist -type f | head -5

# Stage de production
FROM nginx:alpine

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copier les fichiers buildés
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]