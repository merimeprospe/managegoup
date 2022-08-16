# Generated by Django 4.0.4 on 2022-06-24 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projet', '0006_tache_decision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tache',
            name='decision',
            field=models.IntegerField(choices=[(1, 'EN ATTENTE'), (2, 'NULl'), (3, 'PASSABLE'), (4, 'BIEN')], default=1),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenue_log', models.CharField(max_length=300, null=True)),
                ('types_log', models.IntegerField(choices=[(1, 'ajouter'), (2, 'suppression'), (3, 'modification')])),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('user_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_to_user', to=settings.AUTH_USER_MODEL)),
                ('user_projet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projet_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]