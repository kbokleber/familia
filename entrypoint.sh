#!/bin/bash

# Espera o banco de dados estar pronto
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Executa as migrations
echo "Running migrations..."
python manage.py migrate

# Cria um superusuário se não existir
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"

# Coleta arquivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Inicia o servidor
echo "Starting server..."
exec "$@" 