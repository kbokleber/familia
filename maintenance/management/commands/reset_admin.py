from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Redefine a senha do usuário admin'

    def handle(self, *args, **kwargs):
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Senha do admin redefinida com sucesso para "admin123"'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuário admin não encontrado')) 