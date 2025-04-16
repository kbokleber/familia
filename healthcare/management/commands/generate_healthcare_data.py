from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthcare.models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication
from django.utils import timezone
from datetime import timedelta, datetime
import random

class Command(BaseCommand):
    help = 'Gera dados fictícios para o módulo de saúde familiar'

    def handle(self, *args, **kwargs):
        self.stdout.write('Gerando dados fictícios...')

        # Criar membros da família
        family_members = [
            {
                'name': 'João Silva',
                'birth_date': datetime(1980, 5, 15),
                'gender': 'M',
                'relationship': 'Pai',
                'blood_type': 'A+',
                'allergies': 'Nenhuma',
                'chronic_conditions': 'Hipertensão leve',
                'emergency_contact': 'Maria Silva',
                'emergency_phone': '(11) 98765-4321'
            },
            {
                'name': 'Maria Silva',
                'birth_date': datetime(1982, 8, 20),
                'gender': 'F',
                'relationship': 'Mãe',
                'blood_type': 'O+',
                'allergies': 'Penicilina',
                'chronic_conditions': 'Nenhuma',
                'emergency_contact': 'João Silva',
                'emergency_phone': '(11) 98765-4322'
            },
            {
                'name': 'Pedro Silva',
                'birth_date': datetime(2010, 3, 10),
                'gender': 'M',
                'relationship': 'Filho',
                'blood_type': 'A+',
                'allergies': 'Pólen',
                'chronic_conditions': 'Asma',
                'emergency_contact': 'João Silva',
                'emergency_phone': '(11) 98765-4321'
            },
            {
                'name': 'Ana Silva',
                'birth_date': datetime(2012, 12, 25),
                'gender': 'F',
                'relationship': 'Filha',
                'blood_type': 'O+',
                'allergies': 'Nenhuma',
                'chronic_conditions': 'Nenhuma',
                'emergency_contact': 'Maria Silva',
                'emergency_phone': '(11) 98765-4322'
            }
        ]

        for member_data in family_members:
            member, created = FamilyMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Membro da família criado: {member.name}')

        # Criar consultas médicas
        specialties = ['Clínico Geral', 'Pediatria', 'Cardiologia', 'Oftalmologia', 'Dermatologia']
        doctors = [
            'Dr. Carlos Santos',
            'Dra. Ana Oliveira',
            'Dr. Paulo Mendes',
            'Dra. Mariana Costa',
            'Dr. Ricardo Silva'
        ]

        for member in FamilyMember.objects.all():
            for _ in range(random.randint(2, 5)):
                appointment_date = timezone.now() - timedelta(days=random.randint(1, 365))
                next_appointment = appointment_date + timedelta(days=random.randint(30, 90))
                
                MedicalAppointment.objects.create(
                    family_member=member,
                    doctor_name=random.choice(doctors),
                    specialty=random.choice(specialties),
                    appointment_date=appointment_date,
                    location='Hospital São Lucas',
                    reason='Consulta de rotina',
                    diagnosis='Paciente saudável',
                    prescription='Manter hábitos saudáveis',
                    next_appointment=next_appointment,
                    notes='Retorno em 3 meses'
                )

        # Criar procedimentos médicos
        procedures = [
            'Exame de sangue',
            'Raio-X',
            'Ultrassom',
            'Endoscopia',
            'Colonoscopia'
        ]

        for member in FamilyMember.objects.all():
            for _ in range(random.randint(1, 3)):
                procedure_date = timezone.now() - timedelta(days=random.randint(1, 365))
                next_procedure_date = procedure_date + timedelta(days=random.randint(180, 365))
                
                MedicalProcedure.objects.create(
                    family_member=member,
                    procedure_name=random.choice(procedures),
                    procedure_date=procedure_date,
                    doctor_name=random.choice(doctors),
                    location='Hospital São Lucas',
                    description='Procedimento realizado com sucesso',
                    results='Resultados dentro do padrão',
                    follow_up_notes='Acompanhamento em 6 meses',
                    next_procedure_date=next_procedure_date
                )

        # Criar medicamentos
        medications = [
            {
                'name': 'Losartana',
                'dosage': '50mg',
                'frequency': 'once',
                'instructions': 'Tomar pela manhã',
                'side_effects': 'Pode causar tontura'
            },
            {
                'name': 'Paracetamol',
                'dosage': '750mg',
                'frequency': 'as_needed',
                'instructions': 'Tomar em caso de febre',
                'side_effects': 'Nenhum conhecido'
            },
            {
                'name': 'Dipirona',
                'dosage': '500mg',
                'frequency': 'as_needed',
                'instructions': 'Tomar em caso de dor',
                'side_effects': 'Pode causar sonolência'
            },
            {
                'name': 'Vitamina C',
                'dosage': '1000mg',
                'frequency': 'once',
                'instructions': 'Tomar pela manhã',
                'side_effects': 'Nenhum conhecido'
            }
        ]

        for member in FamilyMember.objects.all():
            for med in medications:
                start_date = timezone.now() - timedelta(days=random.randint(1, 365))
                end_date = start_date + timedelta(days=random.randint(30, 90))
                
                Medication.objects.create(
                    family_member=member,
                    name=med['name'],
                    dosage=med['dosage'],
                    frequency=med['frequency'],
                    start_date=start_date,
                    end_date=end_date,
                    prescribed_by=random.choice(doctors),
                    prescription_number=f'RX{random.randint(1000, 9999)}',
                    instructions=med['instructions'],
                    side_effects=med['side_effects'],
                    notes='Medicamento de uso contínuo'
                )

        self.stdout.write(self.style.SUCCESS('Dados fictícios gerados com sucesso!')) 