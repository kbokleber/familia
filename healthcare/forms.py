from django import forms
from .models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication, ProcedureDocument, AppointmentDocument, MedicationDocument, Exam, ExamDocument
from .widgets import MultipleFileInput
from .fields import MultipleFileField

class FamilyMemberForm(forms.ModelForm):
    photo = forms.ImageField(
        required=False,
        label='Foto',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png'
            }
        ),
        help_text='Selecione uma imagem JPG ou PNG'
    )

    class Meta:
        model = FamilyMember
        fields = [
            'name', 'birth_date', 'gender', 'relationship',
            'blood_type', 'allergies', 'chronic_conditions', 'emergency_contact',
            'emergency_phone', 'notes'
        ]
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'birth_date': ['%Y-%m-%d', '%d/%m/%Y'],
        }

class MedicalAppointmentForm(forms.ModelForm):
    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = MedicalAppointment
        fields = [
            'family_member', 'doctor_name', 'specialty', 'appointment_date',
            'location', 'reason', 'diagnosis', 'prescription', 'next_appointment', 'notes'
        ]
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_appointment': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'appointment_date': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
            'next_appointment': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
        }

class MedicalProcedureForm(forms.ModelForm):
    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = MedicalProcedure
        fields = [
            'family_member', 'procedure_name', 'doctor_name', 'procedure_date',
            'next_procedure_date', 'location', 'description', 'results', 'follow_up_notes'
        ]
        widgets = {
            'procedure_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_procedure_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'results': forms.Textarea(attrs={'rows': 3}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'procedure_date': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
            'next_procedure_date': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
        }

class MedicationForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Data e Hora de Início',
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M']
    )
    
    end_date = forms.DateTimeField(
        label='Data e Hora de Término',
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M']
    )

    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = Medication
        fields = [
            'family_member', 'name', 'dosage', 'frequency', 'start_date',
            'end_date', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError({
                'end_date': 'A data e hora de término não podem ser anteriores à data e hora de início.'
            })

        return cleaned_data

class ExamForm(forms.ModelForm):
    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = Exam
        fields = [
            'family_member', 'exam_name', 'doctor_name', 'exam_date',
            'next_exam_date', 'location', 'notes'
        ]
        widgets = {
            'exam_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_exam_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'exam_date': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
            'next_exam_date': ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M'],
        } 