from django import forms
from .models import FamilyMember, MedicalAppointment, MedicalProcedure, Medication

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
        required=True
    )
    
    next_appointment = forms.DateTimeField(
        label='Data da Próxima Consulta',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        required=False
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
        required=True
    )
    
    next_procedure_date = forms.DateTimeField(
        label='Data do Próximo Procedimento',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        required=False
    )

    class Meta:
        model = MedicalProcedure
        fields = ['family_member', 'procedure_name', 'procedure_date',
                 'doctor_name', 'location', 'description', 'results',
                 'follow_up_notes', 'next_procedure_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'results': forms.Textarea(attrs={'rows': 3}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3}),
        }

class MedicationForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Data de Início',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa'
        }),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        help_text='Formato: dd/mm/aaaa',
        required=True
    )
    
    end_date = forms.DateField(
        label='Data de Término',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa'
        }),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        help_text='Formato: dd/mm/aaaa',
        required=False
    )

    class Meta:
        model = Medication
        fields = [
            'family_member', 'name', 'dosage', 'frequency', 'start_date', 'end_date',
            'prescribed_by', 'prescription_number', 'instructions', 'side_effects', 'notes'
        ]
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'side_effects': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        } 