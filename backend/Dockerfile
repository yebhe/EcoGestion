# Dockerfile pour Django
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Vérifier la structure et corriger les permissions
RUN echo "=== Structure du projet ===" && \
    ls -la && \
    echo "=== Contenu backend/ ===" && \
    ls -la backend/ 2>/dev/null || echo "Dossier backend non trouvé" && \
    echo "=== Python path ===" && \
    python -c "import sys; print(sys.path)" && \
    echo "=== Test import backend ===" && \
    python -c "import backend; print('Import backend OK')" 2>/dev/null || echo "Erreur import backend"

# Créer le répertoire pour la base de données SQLite
RUN mkdir -p /app/db

# Exposer le port
EXPOSE 8000

# S'assurer que staticfiles existe et collecter les fichiers
RUN mkdir -p /app/staticfiles && \
    python manage.py collectstatic --noinput --clear || true

# Commande avec collectstatic forcé
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput --clear && gunicorn --bind 0.0.0.0:8000 backend.wsgi:application"]