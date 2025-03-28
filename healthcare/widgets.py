from django.forms import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True 