from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from PIL import Image
import os

class FamilyMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', null=True, blank=True)
    name = models.CharField('Nome', max_length=100)
    photo = models.ImageField('Foto', upload_to='family_members/', null=True, blank=True)
    birth_date = models.DateField('Data de Nascimento')
    gender = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    relationship = models.CharField('Parentesco', max_length=50, null=True, blank=True)
    blood_type = models.CharField('Tipo Sanguíneo', max_length=5, blank=True)
    allergies = models.TextField('Alergias', blank=True)
    chronic_conditions = models.TextField('Condições Crônicas', blank=True)
    emergency_contact = models.CharField('Contato de Emergência', max_length=100, null=True, blank=True)
    emergency_phone = models.CharField('Telefone de Emergência', max_length=20, null=True, blank=True)
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Membro da Família'
        verbose_name_plural = 'Membros da Família'
        ordering = ['name']

    def __str__(self):
        return self.name

class MedicalAppointment(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, verbose_name='Membro da Família')
    doctor_name = models.CharField('Nome do Médico', max_length=100)
    specialty = models.CharField('Especialidade', max_length=100)
    appointment_date = models.DateTimeField('Data da Consulta')
    location = models.CharField('Local', max_length=200, blank=True)
    reason = models.TextField('Motivo da Consulta')
    diagnosis = models.TextField('Diagnóstico', blank=True)
    prescription = models.TextField('Prescrição', blank=True)
    next_appointment = models.DateTimeField('Próxima Consulta', null=True, blank=True)
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Consulta Médica'
        verbose_name_plural = 'Consultas Médicas'
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.family_member.name} - {self.appointment_date.strftime('%d/%m/%Y %H:%M')}"

class MedicalProcedure(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, verbose_name='Membro da Família')
    procedure_name = models.CharField('Nome do Procedimento', max_length=200)
    procedure_date = models.DateTimeField('Data do Procedimento')
    doctor_name = models.CharField('Nome do Médico', max_length=100)
    location = models.CharField('Local', max_length=200, blank=True)
    description = models.TextField('Descrição')
    results = models.TextField('Resultados', blank=True)
    follow_up_notes = models.TextField('Observações de Acompanhamento', blank=True)
    next_procedure_date = models.DateTimeField('Data do Próximo Procedimento', null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Procedimento Médico'
        verbose_name_plural = 'Procedimentos Médicos'
        ordering = ['-procedure_date']

    def __str__(self):
        return f"{self.family_member.name} - {self.procedure_name} ({self.procedure_date.strftime('%d/%m/%Y')})"

class ProcedureDocument(models.Model):
    procedure = models.ForeignKey(MedicalProcedure, on_delete=models.CASCADE, related_name='documents', verbose_name='Procedimento')
    file = models.FileField('Arquivo', upload_to='procedures/documents/')
    name = models.CharField('Nome do Arquivo', max_length=255)
    uploaded_at = models.DateTimeField('Enviado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Documento do Procedimento'
        verbose_name_plural = 'Documentos dos Procedimentos'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} - {self.procedure.procedure_name}"

class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Uma vez ao dia'),
        ('twice', 'Duas vezes ao dia'),
        ('three_times', 'Três vezes ao dia'),
        ('four_times', 'Quatro vezes ao dia'),
        ('every_12h', 'A cada 12 horas'),
        ('every_8h', 'A cada 8 horas'),
        ('every_6h', 'A cada 6 horas'),
        ('every_4h', 'A cada 4 horas'),
        ('as_needed', 'Conforme necessário'),
    ]

    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='medications', verbose_name='Membro da Família')
    name = models.CharField(max_length=100, verbose_name='Nome do Medicamento')
    dosage = models.CharField(max_length=50, verbose_name='Dosagem')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Frequência')
    start_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(null=True, blank=True, verbose_name='Data de Término')
    prescribed_by = models.CharField(max_length=100, blank=True, verbose_name='Prescrito por')
    prescription_number = models.CharField(max_length=50, blank=True, verbose_name='Número da Receita')
    instructions = models.TextField(blank=True, verbose_name='Instruções Especiais')
    side_effects = models.TextField(blank=True, verbose_name='Efeitos Colaterais')
    notes = models.TextField(blank=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.family_member.name}"

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError('A data de término não pode ser anterior à data de início.')

    def get_absolute_url(self):
        return reverse('healthcare:medication_detail', kwargs={'pk': self.pk})

    def is_active(self):
        today = timezone.now().date()
        if self.end_date:
            return self.start_date <= today <= self.end_date
        return self.start_date <= today
