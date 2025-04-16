from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from healthcare.models import FamilyMember, Medication, MedicalAppointment, MedicalProcedure, Exam
from maintenance.models import MaintenanceOrder, Equipment
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Gera dados de teste para todas as tabelas'

    def handle(self, *args, **kwargs):
        self.stdout.write('Gerando dados de teste...')
        
        # Criar usuário admin
        admin, created = User.objects.get_or_create(
            username='admin',
            email='admin@example.com',
            defaults={
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin')
            admin.save()
            self.stdout.write('Usuário admin criado')
        
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='teste',
            email='teste@example.com',
            defaults={
                'first_name': 'Usuário',
                'last_name': 'Teste',
                'is_staff': True
            }
        )
        if created:
            user.set_password('teste123')
            user.save()
            self.stdout.write('Usuário de teste criado')

        # Criar membros da família
        family_members = []
        relationships = ['Pai', 'Mãe', 'Filho', 'Filha', 'Avô', 'Avó']
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        for i in range(5):
            member = FamilyMember.objects.create(
                name=f'Membro da Família {i+1}',
                relationship=random.choice(relationships),
                birth_date=datetime.now() - timedelta(days=random.randint(0, 36500)),
                gender=random.choice(['M', 'F']),
                blood_type=random.choice(blood_types),
                emergency_contact=f'Contato de Emergência {i+1}',
                emergency_phone=f'(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                notes=f'Observações para o membro {i+1}'
            )
            family_members.append(member)
            self.stdout.write(f'Membro da família {i+1} criado')

        # Criar medicamentos
        medications = [
            'Paracetamol', 'Dipirona', 'Omeprazol', 'Losartana', 'Metformina',
            'Atenolol', 'AAS', 'Ibuprofeno', 'Amoxicilina', 'Azitromicina'
        ]
        
        for member in family_members:
            for _ in range(3):
                start_date = datetime.now() - timedelta(days=random.randint(0, 30))
                Medication.objects.create(
                    family_member=member,
                    name=random.choice(medications),
                    dosage=f'{random.randint(1, 10)}mg',
                    frequency=random.choice(['once', 'twice', 'three_times', 'four_times', 'every_12h', 'every_8h', 'every_6h', 'every_4h', 'as_needed']),
                    start_date=start_date,
                    end_date=start_date + timedelta(days=random.randint(7, 30)),
                    prescribed_by='Dr. João Silva',
                    prescription_number=f'RX{random.randint(1000, 9999)}',
                    instructions='Tomar com água',
                    side_effects='Nenhum efeito colateral reportado',
                    notes=f'Medicamento para {member.name}'
                )
            self.stdout.write(f'Medicamentos para {member.name} criados')

        # Criar consultas médicas
        for member in family_members:
            for _ in range(2):
                appointment_date = datetime.now() + timedelta(days=random.randint(1, 30))
                MedicalAppointment.objects.create(
                    family_member=member,
                    doctor_name='Dr. João Silva',
                    specialty='Clínico Geral',
                    appointment_date=appointment_date,
                    location='Hospital São Lucas',
                    reason='Consulta de rotina',
                    diagnosis='Paciente saudável',
                    prescription='Manter hábitos saudáveis',
                    next_appointment=appointment_date + timedelta(days=90),
                    notes=f'Consulta para {member.name}'
                )
            self.stdout.write(f'Consultas para {member.name} criadas')

        # Criar procedimentos médicos
        procedures = [
            'Exame de Sangue', 'Raio-X', 'Tomografia', 'Endoscopia', 'Colonoscopia',
            'Eletrocardiograma', 'Ultrassom', 'Mamografia', 'Densitometria', 'Holter'
        ]
        
        for member in family_members:
            for _ in range(2):
                procedure_date = datetime.now() + timedelta(days=random.randint(1, 30))
                MedicalProcedure.objects.create(
                    family_member=member,
                    procedure_name=random.choice(procedures),
                    procedure_date=procedure_date,
                    doctor_name='Dr. Maria Santos',
                    location='Hospital São Lucas',
                    description='Procedimento de rotina',
                    results='Resultados dentro do normal',
                    follow_up_notes='Acompanhamento em 6 meses',
                    next_procedure_date=procedure_date + timedelta(days=180)
                )
            self.stdout.write(f'Procedimentos para {member.name} criados')

        # Criar exames
        for member in family_members:
            for _ in range(2):
                exam_date = datetime.now() + timedelta(days=random.randint(1, 30))
                Exam.objects.create(
                    family_member=member,
                    exam_name=random.choice(procedures),
                    doctor_name='Dr. Pedro Oliveira',
                    exam_date=exam_date,
                    next_exam_date=exam_date + timedelta(days=90),
                    location='Hospital São Lucas',
                    notes=f'Exame para {member.name}',
                    user=admin
                )
            self.stdout.write(f'Exames para {member.name} criados')

        # Criar equipamentos
        equipment_types = ['eletronico', 'eletrodomestico', 'movel', 'veiculo', 'outro']
        brands = ['Samsung', 'LG', 'Apple', 'Sony', 'Philips', 'Brastemp', 'Electrolux']
        
        equipments = []
        for i in range(5):
            equipment = Equipment.objects.create(
                name=f'Equipamento {i+1}',
                type=random.choice(equipment_types),
                brand=random.choice(brands),
                model=f'Modelo {random.randint(1000, 9999)}',
                serial_number=f'SN{random.randint(10000, 99999)}',
                purchase_date=datetime.now() - timedelta(days=random.randint(0, 365)),
                owner=admin,
                notes=f'Observações para o equipamento {i+1}'
            )
            equipments.append(equipment)
            self.stdout.write(f'Equipamento {i+1} criado')

        # Criar ordens de manutenção
        maintenance_types = ['Preventiva', 'Corretiva', 'Emergencial']
        status_options = ['pendente', 'em_andamento', 'concluida', 'cancelada']
        priority_options = ['baixa', 'media', 'alta', 'urgente']
        
        for equipment in equipments:
            for _ in range(2):
                completion_date = datetime.now() + timedelta(days=random.randint(1, 30))
                MaintenanceOrder.objects.create(
                    equipment=equipment,
                    title=f'Ordem de Manutenção {_+1}',
                    description=f'Descrição da ordem de manutenção {_+1}',
                    status=random.choice(status_options),
                    priority=random.choice(priority_options),
                    service_provider='Empresa de Manutenção XYZ',
                    completion_date=completion_date,
                    cost=random.uniform(100, 1000),
                    warranty_expiration=completion_date + timedelta(days=90),
                    warranty_terms='Garantia de 90 dias para peças e mão de obra',
                    invoice_number=f'NF{random.randint(10000, 99999)}',
                    notes=f'Observações da ordem {_+1}',
                    created_by=admin
                )
            self.stdout.write(f'Ordens de manutenção para {equipment.name} criadas')

        self.stdout.write(self.style.SUCCESS('Dados de teste gerados com sucesso!')) 