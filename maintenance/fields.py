from django import forms
from django.core.validators import FileExtensionValidator

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['multiple'] = True
        self.validators.append(
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx']
            )
        ) 