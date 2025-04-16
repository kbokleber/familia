#!/bin/bash

# Fun��o para esperar o banco de dados
wait_for_db() {
    echo "Waiting for database..."
    export PGPASSWORD=SuaSenhaSeguraParaDB2024!@
    
    for i in {1..30}; do
        if pg_isready -h db -p 5432 -U postgres -d sistema_familiar; then
            echo "Database is ready!"
            return 0
        fi
        echo "Database server is not ready yet... waiting 5 seconds"
        sleep 5
    done
    echo "Could not connect to database after 30 attempts"
    return 1
}

# Espera o banco de dados estar pronto
wait_for_db

if [ $? -eq 0 ]; then
    # Executa as migrations
    echo "Running migrations..."
    python manage.py migrate

    # Cria um superusu�rio se n�o existir
    echo "Creating superuser..."
    python manage.py shell -c "
    from django.contrib.auth import get_user_model;
    User = get_user_model();
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    "

    # Coleta arquivos est�ticos
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # Inicia o servidor
    echo "Starting server..."
    exec "$@"
else
    echo "Failed to connect to database. Exiting..."
    exit 1
fi