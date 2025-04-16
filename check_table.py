import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'maintenance_equipmentattachment'
        );
    """)
    exists = cursor.fetchone()[0]
    print(f"A tabela maintenance_equipmentattachment {'existe' if exists else 'não existe'} no banco de dados.")

    if not exists:
        print("\nTabelas existentes no schema public:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}") 