import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE maintenance_equipmentattachment (
            id bigserial NOT NULL PRIMARY KEY,
            file varchar(100) NOT NULL,
            uploaded_at timestamp with time zone NOT NULL,
            equipment_id bigint NOT NULL REFERENCES maintenance_equipment(id) ON DELETE CASCADE,
            uploaded_by_id integer NULL REFERENCES auth_user(id) ON DELETE SET NULL
        );
        
        CREATE INDEX maintenance_equipmentattachment_equipment_id_idx ON maintenance_equipmentattachment(equipment_id);
        CREATE INDEX maintenance_equipmentattachment_uploaded_by_id_idx ON maintenance_equipmentattachment(uploaded_by_id);
    """)
    print("Tabela maintenance_equipmentattachment criada com sucesso!") 