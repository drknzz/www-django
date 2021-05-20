from django import forms
from django.core.exceptions import ValidationError
from .models import File, Directory

tab_options = {
    "provers": [
        "None",
        "alt-ergo",
        "CVC4",
        "z3"
    ],

    "vcs": [
        "@invariant",
        "@lemma",
        "@ensures",
        "@requires",
        "@assigns",
        "@exits",
        "@assert",
        "@check",
        "@variant",
        "@breaks",
        "@continues",
        "@returns"
    ]
}

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'description', 'directory', 'file']

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if ";" in data:
            raise ValidationError("File name cannot contain semicolon character.")
        return data


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name', 'description', 'parent_directory']


class VCsForm(forms.Form):
    OPTIONS = [
        (1, "@invariant"),
        (2, "@lemma"),
        (3, "@ensures"),
        (4, "@requires"),
        (5, "@assigns"),
        (6, "@exits"),
        (7, "@assert"),
        (8, "@check"),
        (9, "@variant"),
        (10, "@breaks"),
        (11, "@continues"),
        (12, "@returns")
    ]
    vcs = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)