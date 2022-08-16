from django.forms import ModelForm
from django import forms
from .models import Project, Carte, Partenaire, Notification, Tache, Description


class projetform(ModelForm):
    class Meta:
        model = Project
        fields = ['theme']


class carteform(ModelForm):
    class Meta:
        model = Carte
        fields = ['nom_carte']


class tacheform(ModelForm):
    class Meta:
        model = Tache

        fields = ['nom_tache']


class descriptionform(ModelForm):
    class Meta:
        model = Description
        fields = ['sous_tache']


class partenaireform(ModelForm):
    class Meta:
        model = Partenaire
        fields = ['designation']

class notifform(ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'project', 'sender', 'notification', ]