from django import forms

from jat.models import Introduction


class IntroductionForm(forms.ModelForm):
    class Meta:
        model = Introduction
        fields = ['repository', 'version', 'contents', 'access']  # '__all__'
