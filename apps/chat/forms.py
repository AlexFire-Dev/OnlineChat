from django import forms

from .models import Guild, Member


class CreateGuildForm(forms.ModelForm):
    class Meta:
        model = Guild
        fields = ('name', 'poster')
