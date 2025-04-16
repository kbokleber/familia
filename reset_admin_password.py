import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance_project.settings_prod')
django.setup()

User = get_user_model()

# Redefinir senha do superusuário
admin_user = User.objects.filter(username='admin').first()
if admin_user:
    admin_user.set_password('admin')
    admin_user.save()
    print('Senha do superusuário redefinida com sucesso!')
else:
    print('Superusuário não encontrado!') 