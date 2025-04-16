from django import forms
from .models import Equipment, MaintenanceOrder, MaintenanceImage
from .widgets import MultipleFileInput
from .fields import MultipleFileField

class EquipmentForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Anexos'
    )

    class Meta:
        model = Equipment
        fields = ['name', 'type', 'brand', 'model', 'serial_number', 'purchase_date', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'purchase_date': ['%Y-%m-%d', '%d/%m/%Y'],
        }

class MaintenanceOrderForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
        }),
        label='Anexos'
    )

    class Meta:
        model = MaintenanceOrder
        fields = [
            'equipment', 'status', 'service_provider', 'completion_date',
            'cost', 'description', 'warranty_expiration', 'warranty_terms',
            'invoice_number', 'invoice_file', 'notes'
        ]
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiration': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'warranty_terms': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        input_formats = {
            'completion_date': ['%Y-%m-%d', '%d/%m/%Y'],
            'warranty_expiration': ['%Y-%m-%d', '%d/%m/%Y'],
        } 