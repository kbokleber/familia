from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from PIL import Image
import os
import base64
from io import BytesIO

class FamilyMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    name = models.CharField('Nome', max_length=100)
    photo = models.BinaryField('Foto', null=True, blank=True, editable=True)
    photo_type = models.CharField('Tipo da Foto', max_length=10, null=True, blank=True)  # Para armazenar o tipo da imagem (png, jpeg, etc)
    birth_date = models.DateField('Data de Nascimento')
    gender = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    relationship = models.CharField('Parentesco', max_length=50, null=True, blank=True)
    blood_type = models.CharField('Tipo Sanguíneo', max_length=5, blank=True)
    allergies = models.TextField('Alergias', blank=True)
    chronic_conditions = models.TextField('Condições Crônicas', blank=True)
    emergency_contact = models.CharField('Contato de Emergência', max_length=100, null=True, blank=True)
    emergency_phone = models.CharField('Telefone de Emergência', max_length=20, null=True, blank=True)
    notes = models.TextField('Observações', blank=True)
    order = models.IntegerField('Ordem', default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Membro da Família'
        verbose_name_plural = 'Membros da Família'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def set_photo(self, image):
        """
        Recebe um objeto de imagem do Django (InMemoryUploadedFile),
        redimensiona se necessário e salva como dados binários no atributo do modelo.
        A persistência é feita pela chamada .save() na view.
        """
        if image:
            print(f"[DEBUG] Processando imagem: {image.name} - Tamanho: {image.size} bytes")
            print(f"[DEBUG] Tipo do arquivo original: {image.content_type}")
            
            try:
                # Determina o formato baseado na extensão do arquivo
                file_ext = os.path.splitext(image.name)[1].lower()
                if file_ext in ['.jpg', '.jpeg']:
                    save_format = 'jpeg'
                elif file_ext == '.png':
                    save_format = 'png'
                else:
                    print(f"[ERROR] Formato de arquivo não suportado: {file_ext}")
                    return False

                img = Image.open(image)
                print(f"[DEBUG] Imagem aberta com PIL - Modo: {img.mode}, Tamanho: {img.size}")

                # Converte para RGB se necessário
                if img.mode not in ('RGB', 'RGBA'):
                    print(f"[DEBUG] Convertendo imagem de {img.mode} para RGB")
                    img = img.convert('RGB')

                # Redimensiona se a imagem for muito grande
                max_size = (800, 800)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    print(f"[DEBUG] Redimensionando imagem de {img.size} para {max_size}")
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                buffer = BytesIO()
                
                # Salva a imagem no formato apropriado
                if save_format == 'jpeg':
                    img.save(buffer, format='JPEG', quality=85, optimize=True)
                else:  # PNG
                    img.save(buffer, format='PNG', optimize=True)
                
                print(f"[DEBUG] Imagem salva em buffer com formato {save_format.upper()}")
                
                buffer.seek(0)
                self.photo = buffer.getvalue()
                self.photo_type = save_format
                print(f"[DEBUG] Atributos photo e photo_type definidos. Tamanho: {len(self.photo)} bytes, Tipo: {self.photo_type}")
                
                buffer.close()
                return True
            except Exception as e:
                print(f"[ERROR] Erro ao processar imagem: {str(e)}")
                import traceback
                traceback.print_exc()
                self.photo = None
                self.photo_type = None
                return False
        else:
            print("[DEBUG] Nenhuma imagem fornecida, limpando foto existente.")
            self.photo = None
            self.photo_type = None
            return True

    def get_photo_url(self):
        """
        Retorna a URL da foto em formato base64 para exibição em templates.
        Retorna None se não houver foto ou o tipo for inválido.
        """
        if self.photo and self.photo_type:
            try:
                # Verifica se o tipo é suportado
                photo_type = self.photo_type.lower().strip()
                if photo_type not in ['jpeg', 'png']:
                    print(f"[ERROR] Tipo de imagem não suportado: {photo_type}")
                    return None

                # Converte a foto para base64
                photo_base64 = base64.b64encode(self.photo).decode('utf-8')
                
                # Gera a URL com o tipo de imagem correto
                mime_type = 'jpeg' if photo_type == 'jpeg' else 'png'
                url = f"data:image/{mime_type};base64,{photo_base64}"
                print(f"[DEBUG] URL da foto gerada com sucesso. Tipo: {mime_type}")
                return url
            except Exception as e:
                print(f"[ERROR] Erro ao gerar URL da foto: {str(e)}")
                return None
        return None

    @property
    def age(self):
        """Calcula a idade baseada na data de nascimento."""
        if not self.birth_date:
            return None
        today = timezone.now().date()
        age = today.year - self.birth_date.year
        # Ajusta a idade se ainda não fez aniversário este ano
        if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        return age

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
        return f"{self.family_member.name} - {self.doctor_name} - {self.appointment_date.strftime('%d/%m/%Y')}"

class AppointmentDocument(models.Model):
    appointment = models.ForeignKey(MedicalAppointment, on_delete=models.CASCADE, related_name='documents', verbose_name='Consulta')
    file = models.FileField(
        'Arquivo',
        upload_to='appointment_documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    name = models.CharField('Nome do Arquivo', max_length=255)
    uploaded_at = models.DateTimeField('Enviado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Documento da Consulta'
        verbose_name_plural = 'Documentos das Consultas'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} - {self.appointment}"

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
        return f"{self.family_member.name} - {self.procedure_name} - {self.procedure_date.strftime('%d/%m/%Y')}"

class ProcedureDocument(models.Model):
    procedure = models.ForeignKey(MedicalProcedure, on_delete=models.CASCADE, related_name='documents', verbose_name='Procedimento')
    file = models.FileField(
        'Arquivo',
        upload_to='procedure_documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
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
    start_date = models.DateTimeField(verbose_name='Data e Hora de Início')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Data e Hora de Término')
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
        if not self.start_date:
            raise ValidationError('A data e hora de início são obrigatórias.')
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError('A data e hora de término não podem ser anteriores à data e hora de início.')

    def get_absolute_url(self):
        return reverse('healthcare:medication_detail', kwargs={'pk': self.pk})

    def is_active(self):
        if not self.start_date:
            return False
        now = timezone.now()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date <= now

class MedicationDocument(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(
        'Arquivo',
        upload_to='medication_documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        """Verifica se o arquivo é uma imagem"""
        return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

    @property
    def is_document(self):
        """Verifica se o arquivo é um documento"""
        return self.file.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt', '.rtf'))

    def __str__(self):
        return f"{self.name} - {self.medication.name}"

    class Meta:
        verbose_name = 'Documento do Medicamento'
        verbose_name_plural = 'Documentos dos Medicamentos'

class Exam(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=200)
    doctor_name = models.CharField(max_length=100)
    exam_date = models.DateTimeField()
    next_exam_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.family_member.name} - {self.exam_name} - {self.exam_date.strftime('%d/%m/%Y')}"

class ExamDocument(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(
        'Arquivo',
        upload_to='exam_documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.exam}"
