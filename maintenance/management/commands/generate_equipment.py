from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from maintenance.models import Equipment
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Gera equipamentos fictícios para testes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando geração de equipamentos fictícios...')

        # Lista simplificada de equipamentos
        equipment_list = [
            ('Notebook Dell', 'eletronico', 'Dell', 'Inspiron 15', 'SN001'),
            ('Geladeira Brastemp', 'eletrodomestico', 'Brastemp', 'Frost Free', 'SN002'),
            ('Sofá 3 Lugares', 'movel', 'Tok&Stok', 'Retrátil', 'SN003'),
            ('Carro Toyota', 'veiculo', 'Toyota', 'Corolla', 'SN004'),
            ('Ferramentas', 'outro', 'Tramontina', 'Kit Completo', 'SN005')
        ]

        equipments = []
        for name, type, brand, model, serial_number in equipment_list:
            try:
                equipment = Equipment.objects.create(
                    name=name,
                    type=type,
                    brand=brand,
                    model=model,
                    serial_number=serial_number,
                    purchase_date=datetime.now(),
                    notes=f'Equipamento de teste: {name}'
                )
                equipments.append(equipment)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Equipamento criado: {name} - {type}'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Erro ao criar equipamento {name}: {str(e)}'
                    )
                )

        self.stdout.write(self.style.SUCCESS(f'{len(equipments)} equipamentos criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('Geração de equipamentos fictícios concluída com sucesso!')) 