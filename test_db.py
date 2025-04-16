import os
import django
from django.db import connection
from django.conf import settings

# Configurar variáveis de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings')
os.environ['DB_NAME'] = 'sistema_familiar_db'
os.environ['DB_USER'] = 'sistema_familiar_user'
os.environ['DB_PASSWORD'] = 'SuaSenhaSeguraParaDB2024'
os.environ['DB_HOST'] = '89.116.186.192'
os.environ['DB_PORT'] = '5440'

print("Iniciando teste de conexão...")
print(f"Tentando conectar a: {os.environ['DB_HOST']}:{os.environ['DB_PORT']}")
print(f"Banco de dados: {os.environ['DB_NAME']}")
print(f"Usuário: {os.environ['DB_USER']}")

django.setup()

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("\nConexão bem sucedida!")
        print(f"Versão do PostgreSQL: {version[0]}")
        
        # Listar tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print("\nTabelas encontradas:")
        for table in tables:
            print(f"- {table[0]}")
except Exception as e:
    print(f"\nErro ao conectar: {str(e)}")
    print("\nConfiguração atual do banco:")
    print(settings.DATABASES['default']) 