from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from maintenance.models import Equipment, MaintenanceOrder

class Command(BaseCommand):
    help = 'Verifica os usuários e dados no banco'

    def handle(self, *args, **kwargs):
        self.stdout.write('Usuários no banco:')
        for user in User.objects.all():
            self.stdout.write(f'- Username: {user.username}')
            self.stdout.write(f'  Is superuser: {user.is_superuser}')
            self.stdout.write(f'  Is staff: {user.is_staff}')
            self.stdout.write(f'  Date joined: {user.date_joined}')
        
        self.stdout.write('\nEquipamentos no banco:')
        self.stdout.write(f'Total: {Equipment.objects.count()}')
        
        self.stdout.write('\nOrdens de manutenção no banco:')
        self.stdout.write(f'Total: {MaintenanceOrder.objects.count()}') 