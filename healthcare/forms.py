from django import forms
from .models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'photo', 'birth_date', 'gender', 'relationship', 'blood_type',
                 'allergies', 'chronic_conditions', 'emergency_contact',
                 'emergency_phone', 'notes']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'format': '%Y-%m-%d'
            }),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 3}),
        }
        required = ['name', 'birth_date']

class MedicalAppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        label='Data da Consulta',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        required=True,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M']
    )
    
    next_appointment = forms.DateTimeField(
        label='Data da Próxima Consulta',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        required=False,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M']
    )

    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = MedicalAppointment
        fields = ['family_member', 'doctor_name', 'specialty', 'appointment_date',
                 'location', 'reason', 'diagnosis', 'prescription',
                 'next_appointment', 'notes']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalProcedureForm(forms.ModelForm):
    procedure_date = forms.DateTimeField(
        label='Data do Procedimento',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        required=True,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M']
    )
    
    next_procedure_date = forms.DateTimeField(
        label='Data do Próximo Procedimento',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        required=False,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M']
    )

    location = forms.CharField(
        label='Local',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = MedicalProcedure
        fields = ['family_member', 'procedure_name', 'procedure_date',
                 'doctor_name', 'location', 'description', 'results',
                 'follow_up_notes', 'next_procedure_date', 'documents']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'results': forms.Textarea(attrs={'rows': 3}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3}),
        }

class MedicationForm(forms.ModelForm):
    documents = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Documentos'
    )

    class Meta:
        model = Medication
        fields = [
            'family_member', 'name', 'dosage', 'frequency', 'start_date', 'end_date',
            'prescribed_by', 'prescription_number', 'instructions', 'side_effects', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'side_effects': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'start_date': ['%Y-%m-%d', '%d/%m/%Y'],
            'end_date': ['%Y-%m-%d', '%d/%m/%Y'],
        } 