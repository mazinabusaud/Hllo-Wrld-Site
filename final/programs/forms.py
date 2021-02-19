from django import forms
from programs.models import Program
from core.models import UserProfile
from django.core import validators

class NewProgramForm(forms.ModelForm):
    upload = forms.FileField()
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    class Meta():
        model = Program
        fields = ('description','category','upload')

class EditProgramForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    upload = forms.FileField(required=False)
    class Meta():
        model = Program
        fields = ('upload','description', 'category', 'is_public')
        widgets = {'is_public': forms.HiddenInput()}

class OnlyPublicProgramsForm(forms.ModelForm):
    show_public_programs = forms.BooleanField(required = False, label='Show Public Programs', widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit()'}))
    class Meta():
        model = UserProfile
        fields = ['show_public_programs',]
        labels = {
            "show_public_programs": "Show Public Programs"
        }