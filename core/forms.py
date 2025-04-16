from django import forms
from .models import SystemConfig

class SystemConfigForm(forms.ModelForm):
    class Meta:
        model = SystemConfig
        fields = ['key', 'value', 'description']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 