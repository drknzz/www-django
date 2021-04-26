from django import forms
from django.core.exceptions import ValidationError
from .models import File, Directory


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'description', 'directory', 'owner', 'file', 'validity']

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if ";" in data:
            raise ValidationError("File name cannot contain semicolon character.")
        return data


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'description', 'owner', 'parent_directory']