from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verifica o caminho exato do banco de dados'

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']
        self.stdout.write(f'Caminho do banco de dados: {db_path}')
        self.stdout.write(f'O arquivo existe? {os.path.exists(db_path)}')
        if os.path.exists(db_path):
            self.stdout.write(f'Tamanho do arquivo: {os.path.getsize(db_path)} bytes')
            self.stdout.write(f'Última modificação: {os.path.getmtime(db_path)}')
            self.stdout.write(f'Permissões: {oct(os.stat(db_path).st_mode)[-3:]}') 