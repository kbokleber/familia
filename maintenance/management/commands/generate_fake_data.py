from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from maintenance.models import Equipment, MaintenanceOrder
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Gera dados fictícios para teste'

    def handle(self, *args, **kwargs):
        self.stdout.write('Gerando dados fictícios...')

        # Obter o primeiro usuário existente
        try:
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR('Nenhum usuário encontrado. Por favor, crie um usuário primeiro.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar usuário: {str(e)}'))
            return

        # Tipos de equipamentos
        equipment_types = [
            'Ar Condicionado',
            'Refrigerador',
            'Fogão',
            'Máquina de Lavar',
            'Microondas',
            'TV',
            'Computador',
            'Notebook',
            'Impressora',
            'Aspirador de Pó'
        ]

        # Marcas de equipamentos
        brands = [
            'Samsung',
            'LG',
            'Philco',
            'Electrolux',
            'Brastemp',
            'Consul',
            'Panasonic',
            'Dell',
            'HP',
            'Lenovo'
        ]

        # Criar equipamentos
        equipments = []
        for i in range(20):
            equipment = Equipment.objects.create(
                name=f'Equipamento {i+1}',
                type=random.choice(equipment_types),
                brand=random.choice(brands),
                model=f'Modelo {random.randint(1000, 9999)}',
                serial_number=f'SN{random.randint(10000, 99999)}',
                purchase_date=timezone.now() - timedelta(days=random.randint(0, 365*2)),
                owner=user,
                notes=f'Observações para o equipamento {i+1}'
            )
            equipments.append(equipment)

        self.stdout.write(self.style.SUCCESS(f'{len(equipments)} equipamentos criados com sucesso'))

        # Status de manutenção
        status_choices = ['pendente', 'em_andamento', 'concluida']
        
        # Prestadores de serviço
        service_providers = [
            'Assistência Técnica A',
            'Assistência Técnica B',
            'Assistência Técnica C',
            'Assistência Técnica D',
            'Assistência Técnica E'
        ]

        # Criar ordens de manutenção
        maintenance_orders = []
        for i in range(30):
            equipment = random.choice(equipments)
            status = random.choice(status_choices)
            completion_date = None
            if status == 'concluida':
                completion_date = timezone.now() - timedelta(days=random.randint(1, 180))
            
            order = MaintenanceOrder.objects.create(
                equipment=equipment,
                status=status,
                service_provider=random.choice(service_providers),
                completion_date=completion_date,
                cost=random.uniform(100, 1000),
                description=f'Descrição da manutenção {i+1}',
                warranty_expiration=timezone.now() + timedelta(days=random.randint(30, 365)),
                warranty_terms=f'Termos da garantia {i+1}',
                invoice_number=f'NF{random.randint(1000, 9999)}',
                notes=f'Observações da manutenção {i+1}',
                created_by=user
            )
            maintenance_orders.append(order)

        self.stdout.write(self.style.SUCCESS(f'{len(maintenance_orders)} ordens de manutenção criadas com sucesso'))
        self.stdout.write(self.style.SUCCESS('Dados fictícios gerados com sucesso!')) 