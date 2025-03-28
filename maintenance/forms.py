from django import forms
from .models import Equipment, MaintenanceOrder, MaintenanceImage
from .widgets import MultipleFileInput
from .fields import MultipleFileField

class EquipmentForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        label='Anexos'
    )

    class Meta:
        model = Equipment
        fields = ['name', 'type', 'brand', 'model', 'serial_number', 'purchase_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class MaintenanceOrderForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
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
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'service_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'warranty_expiration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'warranty_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_file': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 