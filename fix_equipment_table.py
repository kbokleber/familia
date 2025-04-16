import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings')
django.setup()

with connection.cursor() as cursor:
    # Alterar as colunas para permitir NULL
    cursor.execute("""
        ALTER TABLE maintenance_equipment
        ALTER COLUMN brand DROP NOT NULL,
        ALTER COLUMN model DROP NOT NULL,
        ALTER COLUMN serial_number DROP NOT NULL,
        ALTER COLUMN purchase_date DROP NOT NULL,
        ALTER COLUMN type DROP NOT NULL;
    """)
    print("Tabela maintenance_equipment atualizada com sucesso!")
    
    # Verificar a estrutura da tabela
    cursor.execute("""
        SELECT column_name, is_nullable, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'maintenance_equipment'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    print("\nEstrutura atual da tabela maintenance_equipment:")
    for column in columns:
        print(f"- {column[0]}: {column[2]} (Permite NULL: {column[1]})") 