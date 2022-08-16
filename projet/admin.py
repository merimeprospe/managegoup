from django.contrib import admin

# Register your models here.
from projet.models import Project, Carte, Tache, Description, Partenaire, Notification, Log

admin.site.register(Project)
admin.site.register(Carte)
admin.site.register(Tache)
admin.site.register(Description)
admin.site.register(Partenaire)
admin.site.register(Notification)
admin.site.register(Log)