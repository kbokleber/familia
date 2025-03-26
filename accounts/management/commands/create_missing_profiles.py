from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Cria perfis para usuários que não possuem um'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            try:
                profile = user.profile
                self.stdout.write(self.style.SUCCESS(f'Perfil já existe para o usuário {user.username}'))
            except Profile.DoesNotExist:
                Profile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Perfil criado para o usuário {user.username}')) 