from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verifica as configurações do Django em uso'

    def handle(self, *args, **kwargs):
        self.stdout.write('Configurações atuais do Django:')
        self.stdout.write(f'Settings module: {os.environ.get("DJANGO_SETTINGS_MODULE")}')
        self.stdout.write(f'Database engine: {settings.DATABASES["default"]["ENGINE"]}')
        self.stdout.write(f'Database name: {settings.DATABASES["default"]["NAME"]}')
        self.stdout.write(f'Base dir: {settings.BASE_DIR}')
        self.stdout.write(f'Debug mode: {settings.DEBUG}') 