from django.db import models

# Create your models here.
from personne.models import Account


class Project (models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    theme = models.CharField(max_length=30, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.theme


class Carte (models.Model):
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    nom_carte = models.CharField(max_length=300, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_carte

class Tache (models.Model):
    DECISION = ((1, 'EN ATTENTE'), (2, 'NULl'), (3, 'PASSABLE'), (4, 'BIEN'))
    carte = models.ForeignKey(Carte, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    projet = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    nom_tache = models.CharField(max_length=3000, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    decision = models.IntegerField(choices=DECISION, default=1)

    def __str__(self):
        return self.nom_tache

class Description (models.Model):
    tache = models.ForeignKey(Tache, null=True, on_delete=models.CASCADE)
    sous_tache = models.CharField(max_length=300, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_tache


class Partenaire (models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    designation = models.CharField(max_length=300, null=True, default='partenaire')
    is_active = models.BooleanField(default=False)


    def acceter(sender, instance, *args, **kwargs):
        partenaire = instance
        project = partenaire.project
        sender = partenaire.user
        #accepte = partenaire.partenaire
        notify = Notification(user=project.user, project=project, sender=sender, notification=1)
        notify.save()


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'envoie'), (2, 'accepter'), (3, 'refuser'))

    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE, related_name="noti_from_user")
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, null=True, on_delete=models.CASCADE, related_name="noti_to_user")
    notification = models.IntegerField(choices=NOTIFICATION_TYPES)
    is_seen = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

class Log(models.Model):
    LOG_TYPES = ((1, 'ajouter'), (2, 'suppression'), (3, 'modification'))
    user_projet = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, related_name="projet_to_user")
    user_log = models.ForeignKey(Account, null=True, on_delete=models.CASCADE, related_name="log_to_user")
    contenue_log = models.CharField(max_length=300, null=True)
    types_log = models.IntegerField(choices=LOG_TYPES)
    date_creation = models.DateTimeField(auto_now_add=True)

