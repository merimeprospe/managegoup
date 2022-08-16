from django.db import models

# Create your models here.
from personne.models import Account


class Activite (models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    nom_activite = models.CharField(max_length=300, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_activite