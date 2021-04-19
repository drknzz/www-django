from django import forms

from .models import File, Directory


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'description', 'directory', 'owner', 'file', 'validity']


# class DeleteFileForm(forms.ModelForm):
#     class Meta:
#         model = File
#         fields = ['name']