from django import forms

from .models import Guild, Channel, Member


class CreateGuildForm(forms.ModelForm):
    class Meta:
        model = Guild
        fields = ('name', 'poster')


class CreateChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ('name', 'private')


class UpdateGuildForm(forms.ModelForm):
    class Meta:
        model = Guild
        fields = ('name', 'poster')


class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('admin',)
