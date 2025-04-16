import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings_prod')
django.setup()

User = get_user_model()

# Criar superusuário
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superusuário criado com sucesso!')
else:
    print('Superusuário já existe!') 